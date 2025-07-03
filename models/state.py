#!/usr/bin/python3
"""This is the state class"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
import models
from models.city import City
import shlex


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name: input name
        cities: relationship to City
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade='all, delete, delete-orphan',
                         backref="state")

    @property
    def cities(self):
        """Getter attribute that returns the list of City instances
        with state_id equals to the current State.id
        """
        var = models.storage.all()
        lista = []
        result = []
        for key in var:
            city = key.replace('.', ' ')
            city = shlex.split(city)
            if city[0] == 'City':
                lista.append(var[key])
        for elem in lista:
            if elem.state_id == self.id:
                result.append(elem)
        return result
