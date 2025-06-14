from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from magma.core.database import Base


# ########    SQLALCHEMY MODEL:  employee    ########


class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column("EmployeeId", Integer, primary_key=True, autoincrement=True)
    last_name = Column("LastName", String(20), nullable=False)
    first_name = Column("FirstName", String(20), nullable=False)
    title = Column("Title", String(30))
    reports_to = Column("ReportsTo", Integer, ForeignKey("employees.EmployeeId"))
    birth_date = Column("BirthDate", DateTime(timezone=True))
    hire_date = Column("HireDate", DateTime(timezone=True))
    address = Column("Address", String(70))
    city = Column("City", String(40))
    state = Column("State", String(40))
    country = Column("Country", String(40))
    postal_code = Column("PostalCode", String(10))
    phone = Column("Phone", String(24))
    fax = Column("Fax", String(24))
    email = Column("Email", String(60))

    # RELATIONSHIP - Some employees are also a 'support_rep' and have many 'customers' (who they support):
    # ---- Employee One-to-many Customer (customers) - one employee/support_rep to many customers
    customers = relationship("Customer", back_populates="support_rep")
    # RELATIONSHIP - Some employees are a 'manager' and have 'direct_reports' which are also employees:
    # ---- Employee One-to-many Employee (employees AS direct_reports) - many employees to one employee/manager
    direct_reports = relationship("Employee", backref="manager", remote_side=[employee_id])
    # TODO: remote_side above is giving a type warning in PyCharm. Not something you can import, apparently.


# --------  REFERENCE  --------
# NOTE: In this employee table we have changed from the original schema and made all date/time TIMEZONE AWARE.
# NOTE: Bedrock does not use raw SQL for DB init. SQLAlchemy models are used. This SQL is only here for reference.
# CREATE TABLE employee
# (
#     employee_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     last_name VARCHAR(20) NOT NULL,
#     first_name VARCHAR(20) NOT NULL,
#     title VARCHAR(30),
#     reports_to INT,
#     birth_date TIMESTAMP,
#     hire_date TIMESTAMP,
#     address VARCHAR(70),
#     city VARCHAR(40),
#     state VARCHAR(40),
#     country VARCHAR(40),
#     postal_code VARCHAR(10),
#     phone VARCHAR(24),
#     fax VARCHAR(24),
#     email VARCHAR(60),
#     CONSTRAINT employee_pkey PRIMARY KEY  (employee_id)
# );

