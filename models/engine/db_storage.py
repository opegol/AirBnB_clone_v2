#!/usr/bin/python3
"""Defines functionality for new (DBStorage) engine."""

from models.base_model import BaseModel, Base
from os import getenv
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session


class DBStorage:
    """Represents a database storage engine."""

    __engine = None
    __session = None

    def __init__(self):
        """Initializes new instance of DBStorage."""

        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
    if getenv("HBNB_ENV") == "test":
        Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query current database session for all objects based on the
            given class. if cls=None, query all types of objects
            (User, State, City, Amenity, Place and Review)
        Return:
            dictionary: (like FileStorage)
            key = <class-name>.<object-id>
            value = object
        """
        if cls is None:
            obj = self.__session.query(User).all()
            obj += self.__session.query(State).all()
            obj += self.__session.query(City).all()
            obj += self.__session.query(Amenity).all()
            obj += self.__session.query(Place).all()
            obj += self.__session.query(Review).all()
        else:
            if isinstance(str, type(cls)):
                cls = eval(cls)
            obj = self.__session.query(cls)
        return {f'{type(c).__name__}.{c.id}': c for c in obj}

    def new(self, obj):
        """Add object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from the current database session."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close session."""
        self.__session.close()
