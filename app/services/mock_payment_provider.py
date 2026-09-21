"""
mock_payment_provider.py — plays the role of the payment company.

It sends webhooks to YOUR API exactly the way a real provider would:
  * body is JSON: {event_id, type, reference, amount, currency, paid_at}
  * header X-Signature = HMAC-SHA256(secret, raw body), hex
  * it sometimes sends the SAME event twice (providers retry!)
  * it can send one with a WRONG signature (an attacker)

Usage
-----
  python mock_payment_provider.py --url http://127.0.0.1:8000/api/v1/webhooks/payment \
      --secret mysecret --reference BOOK-123 --amount 45000

  Options:
    --duplicate      send the same event a second time (expects: 200 and no change)
    --bad-signature  also send one with a wrong signature (expects: 401)
    --orphan         also send an event for a reference that does not exist (expects: 200, logged)

Only the standard library is used, so it runs anywhere.
"""
import argparse
import hashlib
import hmac
import json
import sys
import time
import urllib.error
import urllib.request
import uuid


def sign(secret: str, raw_body: bytes) -> str:
    return hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()


def send(url: str, body: dict, signature: str) -> tuple[int, str]:
    raw = json.dumps(body, separators=(",", ":")).encode()
    req = urllib.request.Request(
        url, data=raw, method="POST",
        headers={"Content-Type": "application/json", "X-Signature": signature},
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()
    except urllib.error.URLError as e:
        print(f"  !! could not reach {url}: {e.reason}")
        sys.exit(1)


def make_event(reference: str, amount: int, currency: str = "NGN") -> dict:
    return {
        "event_id": f"evt_{uuid.uuid4().hex[:16]}",
        "type": "payment.succeeded",
        "reference": reference,
        "amount": amount,
        "currency": currency,
        "paid_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def report(label: str, expected: str, status: int, text: str) -> None:
    print(f"{label:<28} -> HTTP {status}   (expected {expected})")
    if text.strip():
        print(f"{'':<28}    body: {text.strip()[:120]}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Mock payment provider — sends signed webhooks.")
    ap.add_argument("--url", required=True, help="your webhook endpoint")
    ap.add_argument("--secret", required=True, help="the WEBHOOK_SECRET your API uses")
    ap.add_argument("--reference", required=True, help="the booking/order/contract reference to confirm")
    ap.add_argument("--amount", type=int, required=True, help="amount in the smallest unit (e.g. kobo)")
    ap.add_argument("--duplicate", action="store_true", help="send the same event twice")
    ap.add_argument("--bad-signature", action="store_true", help="also send one with a wrong signature")
    ap.add_argument("--orphan", action="store_true", help="also send an event for an unknown reference")
    a = ap.parse_args()

    print(f"\nMock provider -> {a.url}\n")

    event = make_event(a.reference, a.amount)
    raw = json.dumps(event, separators=(",", ":")).encode()
    sig = sign(a.secret, raw)

    status, text = send(a.url, event, sig)
    report("1. valid event", "200, confirms once", status, text)

    if a.duplicate:
        time.sleep(0.5)
        status, text = send(a.url, event, sig)          # same event_id, same signature
        report("2. SAME event again (retry)", "200, nothing changes", status, text)

    if a.bad_signature:
        status, text = send(a.url, event, "deadbeef" * 8)
        report("3. wrong signature", "401", status, text)

    if a.orphan:
        orphan = make_event("REF-DOES-NOT-EXIST", a.amount)
        raw_o = json.dumps(orphan, separators=(",", ":")).encode()
        status, text = send(a.url, orphan, sign(a.secret, raw_o))
        report("4. unknown reference", "200, logged as orphan", status, text)

    print("\nNow check your database: the reference must be confirmed exactly once,\n"
          "and processed_events must contain the event_id exactly once.\n")


if __name__ == "__main__":
    main()
