#!/usr/bin/python3
import unittest
import models
from models.user import User
from models.review import Review
from models.amenity import Amenity
from models.state import State
from models.place import Place
from models.city import City
import os


# skip these test if the storage is not db
@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "skip if not fs")
class TestDBStorage(unittest.TestCase):
    """DB Storage test"""

    def setUp(self):
        """ Set up test environment """
        self.storage = models.storage

    def tearDown(self):
        """ Remove storage file at end of tests """
        del self.storage

    def test_user(self):
        """ Tests user """
        user = User(name="Rwigema", email="rwigema@gmail.com", password="Rwigema12345")
        user.save()
        self.assertFalse(user.id in self.storage.all())
        self.assertEqual(user.name, "Rwigema")

    def test_city(self):
        """ test city """
        state = State(name="Texas")
        state.save()
        city = City(name="Austin")
        city.state_id = state.id
        city.save()
        self.assertFalse(city.id in self.storage.all())
        self.assertEqual(city.name, "Austin")

    def test_state(self):
        """ test state"""
        state = State(name="Texas")
        state.save()
        self.assertFalse(state.id in self.storage.all())
        self.assertEqual(state.name, "Texas")

    def test_place(self):
        """Test place"""
        state = State(name="Texas")
        state.save()

        city = City(name="Austin")
        city.state_id = state.id
        city.save()

        user = User(name="Rwigema", email="rwigema@gmail.com", password="Rwigema12345")
        user.save()

        place = Place(name="Palace", number_rooms=4)
        place.city_id = city.id
        place.user_id = user.id
        place.save()

        self.assertFalse(place.id in self.storage.all())
        self.assertEqual(place.number_rooms, 4)
        self.assertEqual(place.name, "Palace")

    def test_amenity(self):
        """ test amenity """
        amenity = Amenity(name="Starlink")
        amenity.save()
        self.assertFalse(amenity.id in self.storage.all())
        self.assertTrue(amenity.name, "Starlink")

    def test_review(self):
        """ test review """
        state = State(name="Texas")
        state.save()

        city = City(name="Austin")
        city.state_id = state.id
        city.save()

        user = User(name="Rwigema", email="rwigema@gmail.com", password="Rwigema12345")
        user.save()

        place = Place(name="Palace", number_rooms=4)
        place.city_id = city.id
        place.user_id = user.id
        place.save()

        review = Review(text="no comment", place_id=place.id, user_id=user.id)
        review.save()

        self.assertFalse(review.id in self.storage.all())
        self.assertEqual(review.text, "no comment")


if __name__ == '__main__':
    unittest.main()
