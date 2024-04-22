#!/usr/bin/python3
""" Place Module for HBNB project """

from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.review import Review
from os import getenv
from sqlalchemy import Integer, String, Table, Column, ForeignKey, Float
from sqlalchemy.orm import relationship


assoc_amenity_table = Table("place_amenity", Base.metadata,
                            Column("place_id", String(60),
                                   ForeignKey("places.id"),
                                   primary_key=True, nullable=False),
                            Column("amenity_id", String(60),
                                   ForeignKey("amenities.id"),
                                   primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ Defines a place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship("Review", backref="place", cascade="delete")
    amenities = relationship("Amenity", secondary="place_amenity", overlaps=                             "place-amenities", viewonly=False)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def reviews(self):
            """returns the list of Review instances with place_id
            equals to the current Place.id.
            """
            rlist = []
            for review in list(models.storage.all(Review).values()):
                if review.place_id == self.id:
                    rlist.append(review)
            return rlist

        @property
        def amenities(self):
            """returns the list of Amenity instances based on the attribute
            amenity_ids that contains all Amenity.id linked to the Place.
            """
            amlist = []
            for amenity in list(models.storage.all(Amenity).values()):
                if amenity.id in self.amenity_ids:
                    amlist.append(amenity)
                return amlist

        @amenities.setter
        def amenities(self, value):
            if isinstance(Amentity, type(value)):
                self.amenity_ids.append(value.id)
