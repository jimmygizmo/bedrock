from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from magma.erp.models.invoice import Invoice
from magma.erp.models.invoice_line import InvoiceLine
from magma.erp.schemas.invoice import InvoiceCreate, InvoiceUpdate


# ########    SERVICE:  invoice    ########


async def get_invoice_service(session: AsyncSession, invoice_id: int) -> Invoice | None:
    statement = (
        select(Invoice)
        .options(
            selectinload(Invoice.customer),
            selectinload(Invoice.invoice_lines).selectinload(InvoiceLine.track)
        )
        .where(Invoice.invoice_id == invoice_id)
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_invoices_service(session: AsyncSession, skip: int = 0, limit: int = 100) -> list[Invoice]:
    statement = (
        select(Invoice)
        .options(
            selectinload(Invoice.customer),
            selectinload(Invoice.invoice_lines).selectinload(InvoiceLine.track)
        )
        .offset(skip)
        .limit(limit)
    )
    result = await session.execute(statement)
    return list(result.scalars().all())  # list() here does nothing but does suppress false static type warnings


async def create_invoice_service(session: AsyncSession, invoice_in: InvoiceCreate) -> Invoice:
    invoice = Invoice(**invoice_in.model_dump())
    session.add(invoice)
    await session.commit()
    await session.refresh(invoice)
    statement = (
        select(Invoice)
        .options(
            selectinload(Invoice.customer),
            selectinload(Invoice.invoice_lines).selectinload(InvoiceLine.track),
        )
        .where(Invoice.invoice_id == invoice.invoice_id)
    )
    result = await session.execute(statement)
    invoice_with_rels = result.scalar_one()

    return invoice_with_rels


# No eager loading (selectinload) needed
async def update_invoice_service(session: AsyncSession, invoice_id: int, invoice_in: InvoiceUpdate) -> Invoice | None:
    invoice = await get_invoice_service(session, invoice_id)
    if not invoice:
        return None

    for field, value in invoice_in.model_dump(exclude_unset=True).items():
        setattr(invoice, field, value)

    await session.commit()
    await session.refresh(invoice)
    return invoice


async def delete_invoice_service(session: AsyncSession, invoice_id: int) -> bool:
    invoice = await get_invoice_service(session, invoice_id)
    if not invoice:
        return False

    await session.delete(invoice)
    await session.commit()
    return True

