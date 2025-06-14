from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from magma.erp.models.customer import Customer
from magma.erp.schemas.customer import CustomerCreate, CustomerUpdate


# ########    SERVICE:  customer    ########


async def get_customer_service(session: AsyncSession, customer_id: int) -> Customer | None:
    statement = (
        select(Customer)
        .options(
            selectinload(Customer.support_rep),
            selectinload(Customer.invoices),
        )
        .where(Customer.customer_id == customer_id)
    )
    result = await session.execute(statement)
    customer = result.scalar_one_or_none()
    return customer


async def get_customers_service(session: AsyncSession, skip: int = 0, limit: int = 100) -> list[Customer]:
    statement = (
        select(Customer)
        .options(
            selectinload(Customer.support_rep),
            selectinload(Customer.invoices),
        )
        .offset(skip)
        .limit(limit)
    )
    result = await session.execute(statement)
    customers = result.scalars().all()
    return list(customers)


async def create_customer_service(session: AsyncSession, customer_in: CustomerCreate) -> Customer:
    customer = Customer(**customer_in.model_dump())
    session.add(customer)
    await session.commit()
    await session.refresh(customer)
    return customer


async def update_customer_service(session: AsyncSession, customer_id: int, customer_in: CustomerUpdate) -> Customer | None:
    customer = await get_customer_service(session, customer_id)
    if not customer:
        return None

    for field, value in customer_in.model_dump(exclude_unset=True, by_alias=True).items():
        setattr(customer, field, value)

    await session.commit()
    await session.refresh(customer)
    return customer


async def delete_customer_service(session: AsyncSession, customer_id: int) -> bool:
    customer = await get_customer_service(session, customer_id)
    if not customer:
        return False

    await session.delete(customer)
    await session.commit()
    return True

