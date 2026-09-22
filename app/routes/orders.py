from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select

from app.models.orders import Order
from app.models.user import Role, User
from app.schemas.order import CreateOrder, OrderOut
from app.services.dependencies import get_current_user, require_role
from app.services.orders import create_order
from app.utils.database import get_session


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post(
    "/",
    response_model=OrderOut,
    status_code=status.HTTP_201_CREATED,
)
def create_customer_order(
    data: CreateOrder,
    session: Session = Depends(get_session),
    current_user: User = Depends(
        require_role(Role.CUSTOMER)
    ),
):
    return create_order(
        session=session,
        customer=current_user,
        data=data,
    )


@router.get(
    "/",
    response_model=list[OrderOut],
)
def list_orders(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == Role.OPS_MANAGER:
        statement = select(Order)
    else:
        statement = select(Order).where(
            Order.customer_id == current_user.id
        )

    return session.exec(statement).all()


@router.get(
    "/{order_id}",
    response_model=OrderOut,
)
def get_order(
    order_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    order = session.get(Order, order_id)

    if order is None:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    if (
        current_user.role != Role.OPS_MANAGER
        and order.customer_id != current_user.id
    ):
        from fastapi import HTTPException

        raise HTTPException(
            status_code=403,
            detail="You do not have permission to view this order",
        )

    return order