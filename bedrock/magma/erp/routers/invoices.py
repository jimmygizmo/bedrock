from fastapi import APIRouter, Depends, HTTPException
from magma.core.logger import log
from magma.core.dependencies import AsyncSessionDep
from magma.erp.schemas.invoice import InvoiceCreate, InvoiceUpdate, InvoiceRead
from magma.erp.services.invoice import *

# ########    ROUTER:  invoice    ########

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.get("/", response_model=list[InvoiceRead])
async def get_invoices(session: AsyncSessionDep, skip: int = 0, limit: int = 100):
    log.info(f"📖 >>>>    /invoices/")
    return await get_invoices_service(session, skip, limit)


@router.get("/{invoice_id}", response_model=InvoiceRead)
async def get_invoice(session: AsyncSessionDep, invoice_id: int):
    log.info(f"👁️ --->    /invoices/{invoice_id}")
    invoice = await get_invoice_service(session, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.post("/", response_model=InvoiceRead, status_code=201)
async def create_invoice(session: AsyncSessionDep, invoice_in: InvoiceCreate):
    log.info(f"☘️ ++++    /invoices/")
    return await create_invoice_service(session, invoice_in)


@router.put("/{invoice_id}", response_model=InvoiceRead)
async def update_invoice(session: AsyncSessionDep, invoice_id: int, invoice_in: InvoiceUpdate):
    log.info(f"✏️ ====    /invoices/{invoice_id}")
    invoice = await update_invoice_service(session, invoice_id, invoice_in)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.delete("/{invoice_id}", status_code=204)
async def delete_invoice(session: AsyncSessionDep, invoice_id: int):
    log.info(f"️💥 ----    /invoices/{invoice_id}")
    success = await delete_invoice_service(session, invoice_id)
    if not success:
        raise HTTPException(status_code=404, detail="Invoice not found")

