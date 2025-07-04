from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Numeric
from sqlalchemy.orm import relationship
from magma.core.database import Base


# ########    SQLALCHEMY MODEL:  invoice    ########


class Invoice(Base):
    __tablename__ = "invoices"

    invoice_id = Column("InvoiceId", Integer, primary_key=True, autoincrement=True)
    customer_id = Column("CustomerId", Integer, ForeignKey("customers.CustomerId"), nullable=False)
    invoice_date = Column("InvoiceDate", DateTime(timezone=True), nullable=False)
    billing_address = Column("BillingAddress", String(70))
    billing_city = Column("BillingCity", String(40))
    billing_state = Column("BillingState", String(40))
    billing_country = Column("BillingCountry", String(40))
    billing_postal_code = Column("BillingPostalCode", String(10))
    total = Column("Total", Numeric(10, 2), nullable=False)

    # RELATIONSHIP - Many 'invoices' can belong to a single 'customer':
    # ---- Invoice Many-to-one Customer (customer) - many invoices to one customer
    customer = relationship("Customer", back_populates="invoices")
    # RELATIONSHIP - An 'invoice' often has multiple 'invoice_lines' from a variety of items being purchased at once:
    # ---- Invoice One-to-many InvoiceLine (invoice_lines) - one invoice to many invoice_lines
    # **** SOLN67 **** DISABLING - see special __init__ file
    # invoice_lines = relationship("InvoiceLine", back_populates="invoice")


# --------  REFERENCE  --------
# NOTE: In this invoice table we have changed from the original schema and made all date/time TIMEZONE AWARE.
# NOTE: Bedrock does not use raw SQL for DB init. SQLAlchemy models are used. This SQL is only here for reference.
# CREATE TABLE invoice
# (
#     invoice_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     customer_id INT NOT NULL,
#     invoice_date TIMESTAMP NOT NULL,
#     billing_address VARCHAR(70),
#     billing_city VARCHAR(40),
#     billing_state VARCHAR(40),
#     billing_country VARCHAR(40),
#     billing_postal_code VARCHAR(10),
#     total NUMERIC(10,2) NOT NULL,
#     CONSTRAINT invoice_pkey PRIMARY KEY  (invoice_id)
# );

