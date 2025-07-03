#!/usr/bin/python3
"""This is the base model class for AirBnB"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import models

Base = declarative_base()

class BaseModel:
    """Defines all common attributes/methods for other classes"""

    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Instantiation of base model class"""
        if kwargs:
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"] and isinstance(value, str):
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.utcnow()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.utcnow()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.utcnow()

    def __str__(self):
        """String representation of the object"""
        return "[{}] ({}) {}".format(type(self).__name__, self.id, self.__dict__)

    def __repr__(self):
        return self.__str__()

    def save(self):
        """Update updated_at and save to storage"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Return dictionary representation of the instance"""
        my_dict = dict(self.__dict__)
        my_dict["__class__"] = self.__class__.__name__
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        my_dict.pop('_sa_instance_state', None)
        return my_dict

    def delete(self):
        """Delete current instance from storage"""
        models.storage.delete(self)
