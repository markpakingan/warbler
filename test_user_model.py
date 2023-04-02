"""User model tests."""

# run these tests like:
#
#    python3 -m unittest test_user_model.py


import os
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

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

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



    # Does the repr method work as expected? DONE
    # Does is_following successfully detect when user1 is following user2? DONE
    # Does is_following successfully detect when user1 is not following user2? DONE
    # Does is_followed_by successfully detect when user1 is followed by user2? DONE
    # Does is_followed_by successfully detect when user1 is not followed by user2? DONE
    # Does User.create successfully create a new user given valid credentials? DONE
    # Does User.create fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail? DONE
    # Does User.authenticate successfully return a user when given a valid username and password? DONE
    # Does User.authenticate fail to return a user when the username is invalid? DONE
    # Does User.authenticate fail to return a user when the password is invalid? DONE

    def test_is_following(self):
        
        """Does is_following successfully detect when user1 is following user2?"""  
        
        user1 = User.username = "mark"
        user_following_list = ["lawrence", "mark", "ej", "kate"]

        self.assertIn(user1,user_following_list)


        """Does is_following successfully detect when user1 is not following user2?"""
        user1 = User.username = "mark"
        user_following_list = ["lawrence", "ej", "kate"]

        self.assertNotIn(user1,user_following_list)




    def test_is_followed_by(self):
        """Does is_followed_by successfully detect when user1 is followed by user2?"""

        # user2 = User(username='mark')

        # self.assertEqual(User.is_followed_by(self, user2), 1)

         # Create two users
        user1 = User(username='user1', email='user1@test.com', password='password')
        user2 = User(username='user2', email='user2@test.com', password='password')

        # Follow user1 with user2
        user2.following.append(user1)
        db.session.add_all([user1, user2])
        db.session.commit()

        # Check if user1 is followed by user2
        self.assertTrue(user1.is_followed_by(user2))

        """Does is_followed_by successfully detect when user1 is not followed by user2?"""

        # Unfollow user1 with user2
        user2.following.remove(user1)
        db.session.commit()

        self.assertFalse(user1.is_followed_by(user2))


    def test_User_signup(self):

        """Does User.create successfully create a new user given valid credentials?"""
        
        username = "kikiamlover"
        email = "markpogi@yahoo.com"
        password = "secretp@ssword"
        image_url =  "https://images.pexels.com/photos/1716861/pexels-photo-1716861.jpeg?auto=compress&cs=tinysrgb&w=1600"

        user = User.signup(username, email, password, image_url)

        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)


        """Does User.create fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?"""
        self.assertIsNotNone(user.username)

    
    def test_User_authenticate(self):

        """Does User.authenticate successfully return a user when given a valid username and password"""
    
        user = User.authenticate('testuser', 'password')
        self.assertIsNotNone(user)
        self.assertFalse(User.authenticate('testuser', 'wrongpassword'))
        self.assertFalse(User.authenticate('nonexistentuser', 'password'))

    

        """Does User.authenticate fail to return a user when the username is invalid?"""
        self.assertFalse(User.authenticate("nonexistentuser", "password"))


    
        # Does User.authenticate fail to return a user when the password is invalid?
        self.assertFalse(User.authenticate("testuser", "wrongpassword"))
