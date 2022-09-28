"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
#python debugger
import pdb
from unittest import TestCase

from models import db, User, Message, Follows, Likes

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

db.create_all()

#opens the python debugger
# pdb.set_trace()


class MessageModelTestCase(TestCase):
    """Test models for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        user1 = User(
            email="test1@test1.com",
            username="testuser1",
            password="password"
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

    
    def test_message_creation(self):
        """Tests creation of new message."""

        msg = Message(text = "test message", user_id = self.user1.id)

        db.session.add(msg)
        db.session.commit()

        self.assertEqual(self.user1.messages[0].text, "test message")

    def test_likes(self):
        """Tests likes of a message."""

        msg = Message(text = "test message", user_id = self.user1.id)
        db.session.add(msg)
        db.session.commit()

        self.user2.likes.append(msg)

        db.session.commit()

        likes = Likes.query.filter(Likes.user_id == self.user2.id).all()
        self.assertEqual(len(likes), 1)