"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
#python debugger
import pdb
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()

#opens the python debugger
# pdb.set_trace()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        user1 = User(
            email="test1@test1.com",
            username="testuser1",
            password="HASHED_PASSWORD"
        )

        user2 = User(
            email="test2@test2.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        self.client = app.test_client()
        self.user1 = user1
        self.user2 = user2

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()


    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
    
    def test_is_following(self):
        """Tests if user is following another user."""

        self.assertEqual(len(self.user1.following), 0)

        self.user1.following.append(self.user2)
        db.session.commit()

        self.assertEqual(len(self.user1.following), 1)
        self.assertEqual(len(self.user2.followers), 1)

    def test_is_followed(self):
        """Tests if user is being followed by another user."""

        self.assertEqual(len(self.user2.followers), 0)

        self.user1.following.append(self.user2)
        db.session.commit()

        self.assertEqual(len(self.user2.followers), 1)



