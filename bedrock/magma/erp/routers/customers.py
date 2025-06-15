from fastapi import APIRouter, HTTPException
from magma.core.logger import log
from magma.core.dependencies import AsyncSessionDep
from magma.erp.schemas.customer import CustomerCreate, CustomerUpdate, CustomerRead
from magma.erp.services.customer import *


# ########    ROUTER:  customer    ########


router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/", response_model=list[CustomerRead])
async def get_customers(session: AsyncSessionDep, skip: int = 0, limit: int = 100):
    log.info(f"📖 >>>>    /customers/    GET ALL")
    return await get_customers_service(session, skip, limit)


@router.get("/{customer_id}", response_model=CustomerRead)
async def get_customer(session: AsyncSessionDep, customer_id: int):
    log.info(f"👁️ --->    /customers/{customer_id}    GET")
    customer = await get_customer_service(session, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.post("/", response_model=CustomerRead, status_code=201)
async def create_customer(session: AsyncSessionDep, customer_in: CustomerCreate):
    log.info(f"☘️ ++++    /customers/    CREATE")
    return await create_customer_service(session, customer_in)


@router.put("/{customer_id}", response_model=CustomerRead)
async def update_customer(session: AsyncSessionDep, customer_id: int, customer_in: CustomerUpdate):
    log.info(f"✏️ ====    /customers/{customer_id}    UPDATE")
    customer = await update_customer_service(session, customer_id, customer_in)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.delete("/{customer_id}", status_code=204)
async def delete_customer(session: AsyncSessionDep, customer_id: int):
    log.info(f"️💥 ----    /customers/{customer_id}    DELETE")
    success = await delete_customer_service(session, customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")

