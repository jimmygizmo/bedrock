from fastapi import APIRouter, Depends, HTTPException
from magma.core.logger import log
from magma.core.dependencies import AsyncSessionDep
from magma.erp.schemas.invoice_line import InvoiceLineCreate, InvoiceLineUpdate, InvoiceLineRead
from magma.erp.services.invoice_line import *

# ########    ROUTER:  invoice_line    ########

router = APIRouter(prefix="/invoice-lines", tags=["invoice_lines"])


@router.get("/", response_model=list[InvoiceLineRead])
async def get_invoice_lines(session: AsyncSessionDep, skip: int = 0, limit: int = 100):
    log.info(f"📖 >>>>    /invoice-lines/    GET ALL")
    return await get_invoice_lines_service(session, skip, limit)


@router.get("/{invoice_line_id}", response_model=InvoiceLineRead)
async def get_invoice_line(session: AsyncSessionDep, invoice_line_id: int):
    log.info(f"👁️ --->    /invoice-lines/{invoice_line_id}    GET")
    invoice_line = await get_invoice_line_service(session, invoice_line_id)
    if not invoice_line:
        raise HTTPException(status_code=404, detail="InvoiceLine not found")
    return invoice_line


@router.post("/", response_model=InvoiceLineRead, status_code=201)
async def create_invoice_line(session: AsyncSessionDep, invoice_line_in: InvoiceLineCreate):
    log.info(f"☘️ ++++    /invoice-lines/    CREATE")
    return await create_invoice_line_service(session, invoice_line_in)


@router.put("/{invoice_line_id}", response_model=InvoiceLineRead)
async def update_invoice_line(session: AsyncSessionDep, invoice_line_id: int, invoice_line_in: InvoiceLineUpdate):
    log.info(f"✏️ ====    /invoice-lines/{invoice_line_id}    UPDATE")
    invoice_line = await update_invoice_line_service(session, invoice_line_id, invoice_line_in)
    if not invoice_line:
        raise HTTPException(status_code=404, detail="InvoiceLine not found")
    return invoice_line


@router.delete("/{invoice_line_id}", status_code=204)
async def delete_invoice_line(session: AsyncSessionDep, invoice_line_id: int):
    log.info(f"💥 ----    /invoice-lines/{invoice_line_id}    DELETE")
    success = await delete_invoice_line_service(session, invoice_line_id)
    if not success:
        raise HTTPException(status_code=404, detail="InvoiceLine not found")

