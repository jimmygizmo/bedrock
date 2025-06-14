from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, TYPE_CHECKING
# from magma.erp.schemas.genre import GenreRead
# from magma.erp.schemas.media_type import MediaTypeRead
# from magma.erp.schemas.invoice_line import InvoiceLineRead
# from magma.erp.schemas.playlist_track import PlaylistTrackRead


# ########    PYDANTIC SCHEMA:  track    ########


# --------  CONFIG  --------
class ConfigBase(BaseModel):
    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


# --------  BASE  --------
class TrackBase(ConfigBase):
    name: str = Field(..., alias="Name")
    album_id: Optional[int] = Field(None, alias="AlbumId")
    media_type_id: int = Field(..., alias="MediaTypeId")
    genre_id: Optional[int] = Field(None, alias="GenreId")
    composer: Optional[str] = Field(None, alias="Composer")
    milliseconds: int = Field(..., alias="Milliseconds")
    bytes: Optional[int] = Field(None, alias="Bytes")
    unit_price: float = Field(..., alias="UnitPrice")


# --------  CREATE (POST)  --------
class TrackCreate(TrackBase):
    # TODO: /magma/validators/shared.py has two validator examples there intended to use HERE. Complete and implement.
    pass


# --------  UPDATE (PUT)  --------
class TrackUpdate(ConfigBase):
    name: Optional[str] = None
    album_id: Optional[int] = None
    media_type_id: Optional[int] = None
    genre_id: Optional[int] = None
    composer: Optional[str] = None
    milliseconds: Optional[int] = None
    bytes: Optional[int] = None
    unit_price: Optional[float] = None


# --------  READ (GET)  -  (Early, in-progress developing relation views.)  FLAT, NO JOINS  --------
class TrackRead(ConfigBase):
    track_id: int
    name: str
    album_id: Optional[int]
    media_type_id: int
    genre_id: Optional[int]
    composer: Optional[str]
    milliseconds: int
    bytes: Optional[int]
    unit_price: float


# TODO: IMPORTANT FEATURE - CONTROL DETAIL LEVELS IN ENDPOINT OUTOUT - URL?detail=basic  vs.  URL?detail=full
# Example of how we would implement this in the router:
# @router.get("/users/", response_model=List[UserReadBasic])
# def list_users(detail: str = Query("basic")):
#     if detail == "full":
#         return user_service.get_users_full()
#     return user_service.get_users_basic()
# TODO: So we would have different services and different combinations of special READ schemas, likely residing in
#   models.erp.shared. The URL?param=value technique avoids excessive @router definitions and endpoint/API overgrowth.
#   Now it is also arguable that some special cases could deserve their own URL path or path component such as:
#   /resource/detailed/ but that needs to be carefully considered and would be hard to do while also being consistent
#   for your entire API if it is or will grow to being of any significant size.
#   The URL?param technique is growth-friendly, while using path components like /resource/detailed/ is growth-complex.
# THIS COMMENT IS REPEATED IN THE TRACK ROUTER - CLEAN UP LATER AFTER IMPLEMENTING AT LEAST ONE EXAMPLE OF THIS.

# ANOTHER EXAMPLE:
# @router.get("/invoices/")
# def list_invoices(
#     view: str = Query("summary", enum=["summary", "ledger-report", "export"]),
#     db: Session = Depends(get_db)
# ):
#     if view == "summary":
#         return invoice_service.get_invoices_summary(db)
#     elif view == "ledger-report":
#         return invoice_service.get_invoices_ledger_report(db)
#     elif view == "export":
#         return invoice_service.get_invoices_export(db)
#     else:
#         raise HTTPException(status_code=400, detail="Invalid view name")

# AND THE SERVICES FOR THIS EXAMPLE:
# from magma.models import Invoice
# from magma.schemas.invoice import (
#     InvoiceSummary,
#     InvoiceLedgerReport,
#     InvoiceExport,
# )
#
# def get_invoices_summary(db) -> list[InvoiceSummary]:
#     # ORM query, mapped to summary schema
#     ...
#
# def get_invoices_ledger_report(db) -> list[InvoiceLedgerReport]:
#     # ORM query + joins + aggregation for report view
#     ...
#
# def get_invoices_export(db) -> list[InvoiceExport]:
#     # ORM query + formatting for export
#     ...

# AND THE SCHEMA FOR THIS EXAMPLE:
# # ---------- Base model ----------
# class InvoiceBase(BaseModel):
#     id: int
#     customer_id: int
#     total: Decimal
#     invoice_date: date
#
# # ---------- View: summary ----------
# class InvoiceSummary(InvoiceBase):
#     pass  # just basic fields, inherited
#
# # ---------- View: ledger report ----------
# class InvoiceLedgerReport(InvoiceBase):
#     line_items: List[dict]  # or List[InvoiceLineLedgerSchema]
#
# # ---------- View: export ----------
# class InvoiceExport(InvoiceBase):
#     customer_name: str
#     currency: str
#     exported_at: datetime


# IN-PROGRESS WORK:
# TODO: Related to other issues but seen here . Notice we set some related reads to None. CONFIRM, This effectively
#   excludes just their value or the key also from the output (JSON)? Also, what was the other issue this was related to?
#   This was mentioned as a way of solving some other issue without affecting the Read output, something maybe related
#   to a nested loop in lazy loading?  Possibly as an alternative to removing the var/related-record entirely becuase
#   that leads to some other problem, possibly as mild as a PyCharm warning if I recall. Anyhow I think this is not
#   needed just worth understanding for future reference, because the actual solution is to force eager loading of
#   related records in the service using selectinload or similar. I'm keeping this example here for a few other reasons
#   too. TODO: Document all this knowledge formally elsewhere.
#
# EXAMPLE OF A JOIN SCHEMA
# UPDATE: The app has working examples like this now. This one will be the most complex set of joins when we implement.
#   More specifically, there are likely to be multiple variations:  URL?detail=basic  URL?detail=medium  URL?detail=full
#   * OR we could tailor them to specific views:  URL?detail=invoice-view  URL?detail=ledger-report-view
#   * OR even better:  URL?view=invoice  URL?view=ledger-report
#   ** TODO: This is a very nice pattern. Find out how common it might be.
# Uses imported schemas: AlbumRead, MediaTypeRead, GenreRead, InvoiceLineRead, PlayListTrackRead
# class TrackDeepRead(BaseModel):  # "deep read" - includes relationships
#     track_id: int
#     name: str
#     album_id: Optional[int]
#     media_type_id: int
#     genre_id: Optional[int]
#     composer: Optional[str]
#     milliseconds: int
#     bytes: Optional[int]
#     unit_price: float
#
#     album: Optional[AlbumRead] = None
#     media_type: Optional[MediaTypeRead] = None
#     genre: Optional[GenreRead] = None
#     invoice_lines: Optional[List[InvoiceLineRead]] = []
#     playlists: Optional[List[PlaylistTrackRead]] = []
#
#     class Config:
#         from_attributes = True
#         populate_by_name = True


# --------  REFERENCE  --------
# NOTE: Bedrock does not use raw SQL for DB init. SQLAlchemy models are used. This SQL is only here for reference.
# CREATE TABLE track
# (
#     track_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     name VARCHAR(200) NOT NULL,
#     album_id INT,
#     media_type_id INT NOT NULL,
#     genre_id INT,
#     composer VARCHAR(220),
#     milliseconds INT NOT NULL,
#     bytes INT,
#     unit_price NUMERIC(10,2) NOT NULL,
#     CONSTRAINT track_pkey PRIMARY KEY  (track_id)
# );

