"""Message model tests"""


import os
from unittest import TestCase

from models import db, User, Message, Follows, Likes

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


from app import app

db.create_all()


class MessageModelTestCase(TestCase):

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()


    class UserModelTestCase(TestCase):
        """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.uid = 94566
        u = User.signup("testing", "testing@test.com", "password", None)
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    

    def test_message_model(self):
        """Does basic model work?"""
        
        m = Message(
            text="a warble",
            user_id=self.uid
        )

        db.session.add(m)
        db.session.commit()

        # User should have 1 message
        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(self.u.messages[0].text, "a warble")

    def test_message_likes(self):
        m1 = Message(text = "this is a test", 
                     user_id = self.uid)
        
        m2 = Message(text = "this is the 2nd message", 
                     user_id = self.uid)
        
        u = User.signup(username = "usertest", email = "test@yahoo.com", password="p@ssword",
                        image_url="https://images.pexels.com/photos/3687770/pexels-photo-3687770.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1")

        uid = 123

        u.id = uid
        
        db.session.add_all([m1, m2, u])
        db.session.commit()

        u.likes.append(m1)

        db.session.commit()

        l = Likes.query.filter(Likes.user_id == uid).all()

        self.assertEqual(len(l),1)
        self.assertEqual(l[0].message_id, m1.id)

    

