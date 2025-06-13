from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from magma.core.database import Base


# ########    SQLALCHEMY MODEL:  customer    ########


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column("CustomerId", Integer, primary_key=True, autoincrement=True)
    first_name = Column("FirstName", String(40), nullable=False)
    last_name = Column("LastName", String(20), nullable=False)
    company = Column("Company", String(80))
    address = Column("Address", String(70))
    city = Column("City", String(40))
    state = Column("State", String(40))
    country = Column("Country", String(40))
    postal_code = Column("PostalCode", String(10))
    phone = Column("Phone", String(24))
    fax = Column("Fax", String(24))
    email = Column("Email", String(60), nullable=False)
    support_rep_id = Column("SupportRepId", Integer, ForeignKey("employees.EmployeeId"))

    # RELATIONSHIP - Many 'customers' can be assigned to an 'employee' who is also a 'support_rep':
    # ---- Customer Many-to-one Employee (employee AS support_rep) - many 'customers' to one 'employee'/'support_rep'
    support_rep = relationship("Employee", back_populates="customers")
    # RELATIONSHIP - A 'customer' can have many 'invoices', one from each purchase they made:
    # ---- Customer One-to-many Invoice (invoices) - one customer to many invoices
    invoices = relationship("Invoice", back_populates="customer")


# --------  REFERENCE  --------
# NOTE: Bedrock does not use raw SQL for DB init. SQLAlchemy models are used. This SQL is only here for reference.
# CREATE TABLE customer
# (
#     customer_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     first_name VARCHAR(40) NOT NULL,
#     last_name VARCHAR(20) NOT NULL,
#     company VARCHAR(80),
#     address VARCHAR(70),
#     city VARCHAR(40),
#     state VARCHAR(40),
#     country VARCHAR(40),
#     postal_code VARCHAR(10),
#     phone VARCHAR(24),
#     fax VARCHAR(24),
#     email VARCHAR(60) NOT NULL,
#     support_rep_id INT,
#     CONSTRAINT customer_pkey PRIMARY KEY  (customer_id)
# );

