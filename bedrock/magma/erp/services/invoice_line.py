from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from magma.erp.models.invoice_line import InvoiceLine
from magma.erp.models.track import Track
from magma.erp.schemas.invoice_line import InvoiceLineCreate, InvoiceLineUpdate


# ########    SERVICE:  invoice_line    ########


async def get_invoice_line_service(session: AsyncSession, invoice_line_id: int) -> InvoiceLine | None:
    statement = (
        select(InvoiceLine)
        .options(selectinload(InvoiceLine.track))
        .where(InvoiceLine.invoice_line_id == invoice_line_id)
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_invoice_lines_service(session: AsyncSession, skip: int = 0, limit: int = 100) -> list[InvoiceLine]:
    statement = (
        select(InvoiceLine)
        .options(selectinload(InvoiceLine.track))
        .offset(skip)
        .limit(limit)
    )
    result = await session.execute(statement)
    return list(result.scalars().all())  # list() here does nothing but does suppress false static type warnings


async def create_invoice_line_service(session: AsyncSession, invoice_line_in: InvoiceLineCreate) -> InvoiceLine:
    invoice_line = InvoiceLine(**invoice_line_in.model_dump())
    session.add(invoice_line)
    await session.commit()
    await session.refresh(invoice_line)

    statement = (
        select(InvoiceLine)
        .options(selectinload(InvoiceLine.track))
        .where(InvoiceLine.invoice_line_id == invoice_line.invoice_line_id)
    )
    result = await session.execute(statement)
    invoice_line_with_rels = result.scalar_one()

    return invoice_line_with_rels


# No eager loading (selectinload) needed
async def update_invoice_line_service(session: AsyncSession, invoice_line_id: int, invoice_line_in: InvoiceLineUpdate) -> InvoiceLine | None:
    invoice_line = await get_invoice_line_service(session, invoice_line_id)
    if not invoice_line:
        return None

    for field, value in invoice_line_in.model_dump(exclude_unset=True).items():
        setattr(invoice_line, field, value)

    await session.commit()
    await session.refresh(invoice_line)
    return invoice_line


async def delete_invoice_line_service(session: AsyncSession, invoice_line_id: int) -> bool:
    invoice_line = await get_invoice_line_service(session, invoice_line_id)
    if not invoice_line:
        return False

    await session.delete(invoice_line)
    await session.commit()
    return True

