from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from magma.erp.models.employee import Employee
from magma.erp.schemas.employee import EmployeeCreate, EmployeeUpdate


# ########    SERVICE:  employee    ########


async def get_employee_service(session: AsyncSession, employee_id: int) -> Employee | None:
    statement = (
        select(Employee)
        .options(
            selectinload(Employee.direct_reports),
            selectinload(Employee.manager),
        )
        .where(Employee.employee_id == employee_id)
    )
    result = await session.execute(statement)
    employee = result.scalar_one_or_none()
    return employee


async def get_employees_service(session: AsyncSession, skip: int = 0, limit: int = 100) -> list[Employee]:
    statement = (
        select(Employee)
        .options(
            selectinload(Employee.direct_reports),
            selectinload(Employee.manager),
        )
        .offset(skip)
        .limit(limit)
    )
    result = await session.execute(statement)
    employees = result.scalars().all()
    return list(employees)


# NOTE: This method works fine without the need for selectinload
async def create_employee_service(session: AsyncSession, employee_in: EmployeeCreate) -> Employee:
    employee = Employee(**employee_in.model_dump())
    session.add(employee)
    await session.commit()
    await session.refresh(employee)
    return employee


# NOTE: This method works fine without the need for selectinload
async def update_employee_service(session: AsyncSession, employee_id: int, employee_in: EmployeeUpdate) -> Employee | None:
    employee = await get_employee_service(session, employee_id)
    if not employee:
        return None

    for field, value in employee_in.model_dump(exclude_unset=True).items():
        setattr(employee, field, value)

    await session.commit()
    await session.refresh(employee)
    return employee


async def delete_employee_service(session: AsyncSession, employee_id: int) -> bool:
    employee = await get_employee_service(session, employee_id)
    if not employee:
        return False

    await session.delete(employee)
    await session.commit()
    return True

