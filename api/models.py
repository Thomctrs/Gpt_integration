from sqlalchemy import Column, Integer, String, Float, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship,joinedload
from .database import Base



class Brand(Base):
    __tablename__ = "brands"

    brand_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    founded_year = Column(Integer)
    country = Column(String(100))

    # Relation avec les collections et montres
    collections = relationship("Collection", back_populates="brand")
    watches = relationship("Watch", back_populates="brand")


class Collection(Base):
    __tablename__ = "collections"

    collection_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.brand_id"))

    # Relations
    brand = relationship("Brand", back_populates="collections")
    watches = relationship("Watch", back_populates="collection")


class Watch(Base):
    __tablename__ = "watches"

    watch_id = Column(Integer, primary_key=True, index=True)
    model = Column(String(150), nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.brand_id"))
    collection_id = Column(Integer, ForeignKey("collections.collection_id"))
    price = Column(Float, nullable=False)
    description = Column(Text)
    technical_details = Column(Text)
    reference_number = Column(String(50))
    movement_type = Column(String(50))
    case_material = Column(String(50))
    water_resistance = Column(Integer)
    diameter = Column(Float)
    stock_quantity = Column(Integer)

    # Relations
    brand = relationship("Brand", back_populates="watches")
    collection = relationship("Collection", back_populates="watches")
    images = relationship("Image", back_populates="watch")


class Image(Base):
    __tablename__ = "images"

    image_id = Column(Integer, primary_key=True, index=True)
    watch_id = Column(Integer, ForeignKey("watches.watch_id"))
    image_url = Column(String(255), nullable=False)
    is_primary = Column(Boolean, default=False)

    # Relation
    watch = relationship("Watch", back_populates="images")
