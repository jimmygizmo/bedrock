from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from magma.core.database import Base


# ########    SQLALCHEMY MODEL:  invoice_line    ########


class InvoiceLine(Base):
    __tablename__ = "invoice_lines"

    invoice_line_id = Column("InvoiceLineId", Integer, primary_key=True, autoincrement=True)
    invoice_id = Column("InvoiceId", Integer, ForeignKey("invoices.InvoiceId"), nullable=False)
    track_id = Column("TrackId", Integer, ForeignKey("tracks.TrackId"), nullable=False)
    unit_price = Column("UnitPrice", Numeric(10, 2), nullable=False)
    quantity = Column("Quantity", Integer, nullable=False)

    # RELATIONSHIP - Many 'invoice_lines' can belong to a single 'invoice' when they are purchased together:
    # ---- InvoiceLine Many-to-one Invoice (invoice) - many 'invoice_lines' to one 'invoice'
    invoice = relationship("Invoice", back_populates="invoice_lines")
    # RELATIONSHIP - Many 'invoice_lines' can be for a single 'track' because many copies of a 'track' can be sold:
    # ---- InvoiceLine Many-to-one Track (track) - many invoice_lines to one track
    track = relationship("Track", back_populates="invoice_lines")


# SQL CREATE from the original Chinook project for comparison with this Bedrock model
#
# CREATE TABLE invoice_line
# (
#     invoice_line_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     invoice_id INT NOT NULL,
#     track_id INT NOT NULL,
#     unit_price NUMERIC(10,2) NOT NULL,
#     quantity INT NOT NULL,
#     CONSTRAINT invoice_line_pkey PRIMARY KEY  (invoice_line_id)
# );

