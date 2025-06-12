from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from magma.core.database import Base


# ########    SQLALCHEMY MODEL:  media_type    ########


class MediaType(Base):
    __tablename__ = "media_types"

    media_type_id = Column("MediaTypeId", Integer, primary_key=True, autoincrement=True)
    name = Column("Name", String(120))

    # RELATIONSHIP - A 'media_type' has multiple 'tracks' which are categorized as being of that 'media_type':
    # ---- MediaType One-to-many Track (tracks) - one media_type to many tracks
    tracks = relationship("Track", back_populates="media_type")


# SQL CREATE from the original Chinook project for comparison with this Bedrock model
#
# CREATE TABLE media_type
# (
#     media_type_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     name VARCHAR(120),
#     CONSTRAINT media_type_pkey PRIMARY KEY  (media_type_id)
# );

