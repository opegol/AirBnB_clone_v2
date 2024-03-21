#!/usr/bin/python3
"""State Module for HBNB project."""
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.city import City
from os import getenv


class State(BaseModel, Base):
    """Maps State class to states Table in MySQl database"""

    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='state', cascade='delete')

    if getenv('HNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """returns the list of City instances with state_id equals
            to the current State.id.
            It will be the FileStorage relationship between State and City.
            """
            cty = []
            for city in list(storage.all(City).values()):
                if city.state_id == self.id:
                    cty.append(city)
            return cty
