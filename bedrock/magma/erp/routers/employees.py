from fastapi import APIRouter, Depends, HTTPException
from magma.core.logger import log
from magma.core.dependencies import AsyncSessionDep
from magma.erp.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeRead
from magma.erp.services.employee import *


# ########    ROUTER:  employee    ########


router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/", response_model=list[EmployeeRead])
async def get_employees(session: AsyncSessionDep, skip: int = 0, limit: int = 100):
    log.info(f"📖 >>>>    /employees/")
    return await get_employees_service(session, skip, limit)


@router.get("/{employee_id}", response_model=EmployeeRead)
async def get_employee(session: AsyncSessionDep, employee_id: int):
    log.info(f"👁️ --->    /employees/{employee_id}")
    employee = await get_employee_service(session, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.post("/", response_model=EmployeeRead, status_code=201)
async def create_employee(session: AsyncSessionDep, employee_in: EmployeeCreate):
    log.info(f"☘️ ++++    /employees/")
    return await create_employee_service(session, employee_in)


@router.put("/{employee_id}", response_model=EmployeeRead)
async def update_employee(session: AsyncSessionDep, employee_id: int, employee_in: EmployeeUpdate):
    log.info(f"✏️ ====    /employees/{employee_id}")
    employee = await update_employee_service(session, employee_id, employee_in)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.delete("/{employee_id}", status_code=204)
async def delete_employee(session: AsyncSessionDep, employee_id: int):
    log.info(f"💥 ----    /employees/{employee_id}")
    success = await delete_employee_service(session, employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")

