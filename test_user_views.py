"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py


import os
import pdb
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        user1 = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.add(user1)
        db.session.commit()

        user2 = User.signup(username="cooltesting",
        email = "test2@test2.com",
        password = "test2user",
        image_url = None)

        db.session.add(user2)
        db.session.commit()

        self.user1 = user1
        self.user2 = user2

    def tearDown(self):
        """Tear down fouled transactions."""
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_list_users(self):
        """Test for showing list of users."""

        with self.client as c:
            resp = c.get("/users")

            self.assertIn("testuser", str(resp.data))
            self.assertIn("cooltesting", str(resp.data))

    def test_users_show(self):
        """Test for showing a specific user."""

        msg = Message(text = "messsage", user_id = self.user1.id)
        db.session.add(msg)
        db.session.commit()

        with self.client as c:
            resp = c.get(f"/users/{self.user1.id}")

            self.assertIn("testuser", str(resp.data))
            self.assertIn("message", str(resp.data))
            self.assertNotIn("cooltesting", str(resp.data))

    def test_show_following(self):
        """Test for showing who a user follows."""
        self.user1.following.append(self.user2)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp = c.get(f"/users/{self.user1.id}/following", follow_redirects = True)

            self.assertIn("@cooltesting", str(resp.data))

    def test_users_following(self):
        """Test for showing who is following a user."""
        self.user1.following.append(self.user2)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user2.id

            resp = c.get(f"/users/{self.user2.id}/followers", follow_redirects = True)

            self.assertIn("@testuser", str(resp.data))

    def test_add_like(self):
        """Test for liking a message."""        
        msg = Message(id = 1111, text = "message!!!", user_id = self.user2.id)
        db.session.add(msg)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id
            
            resp = c.post(f"/like/1111", follow_redirects = True)

            self.assertIn("message!!!", str(resp.data))

    def test_profile(self):
        """Test for updating user profile."""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id
            
            resp = c.post("/users/profile", data={"username": "newname", "password" : self.user1.password}, follow_redirects = True)

            self.assertIn("newname", str(resp.data))

            resp = c.post("/users/profile", data={"username": "anothername", "password" : "incorrect"})

            self.assertIn("Incorrect password.", str(resp.data))
    
    def test_delete_user(self):
        """Test for deleting a user."""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp = c.post("/users/delete", follow_redirects = True)

            self.assertIn("Join Warbler today.", str(resp.data))

            deleted_user = User.query.get(self.user1.id)

            self.assertIsNone(deleted_user)                  

