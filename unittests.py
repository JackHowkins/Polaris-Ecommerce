import os
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        #the basedir lines could be added like the original db
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()
        pass

    def tearDown(self):
        pass

    # Ensure flask is set up correctly
    def test_addtaskroute(self):
        tester = app.test_client(self)
        home = tester.get('/',follow_redirects=True)
        self.assertEqual(home.status_code, 200)

    # Register with all the correct rules
    # Should create the account and then redirect to login page - which has the text in 'assertIn' on
    def test_succesful_register(self):
        tester = app.test_client(self)
        response = self.app.post('/sign-up',
                                data={'firstname': 'none', 'surname': 'none', 'email': 'none@none.com', 'password': 'none11'},
                                follow_redirects=True)
        added = models.Customers.query.filter_by(email='none@none.com').all()
        self.assertEqual(added[0].email, 'none@none.com')
        self.assertIn(b'Not signed up yet?', response.data)

    # Register with an email of the incorrect type
    # Should not create the account and should flash an error
    def test_register_incorrect_email(self):
        tester = app.test_client(self)
        response = self.app.post('/sign-up',
                                data={'firstname': 'none', 'surname': 'none', 'email': 'none', 'password': 'none11'},
                                follow_redirects=True) # Populates fields with incorrect sign up data
        added = models.Customers.query.filter_by(email='none').all() # Tries to find the 'none' email in the database - it shouldnt have been added
        self.assertEqual(0, len(added)) # If the length of added (should be 0) and 0 are equal
        self.assertIn(b'ERROR: Not a valid email address', response.data) # Checks that the HTML page has 'NOT A VALID EMAIL ADDRESS' in it

    # Register with a password that is too small
    # Should not create the account and should flash an error about the password
    def test_register_small_pass(self):
        tester = app.test_client(self)
        response = self.app.post('/sign-up',
                                data={'firstname': 'none', 'surname': 'none', 'email': 'none2@none.com', 'password': 'a'},
                                follow_redirects=True)
        added = models.Customers.query.filter_by(password='a').all()
        self.assertEqual(0, len(added))
        self.assertIn(b'password must be more than 6 characters', response.data)

    # Try to re-register with the same email
    # Should not create the account as you are already registered and redirect to the sign in
    def test_re_register(self):
        tester = app.test_client(self)
        response = self.app.post('/sign-up',
                                data={'firstname': 'none', 'surname': 'none', 'email': 'none@none.com', 'password': 'a'},
                                follow_redirects=True)
        self.assertIn(b'ERROR: You are already registered', response.data)

    # Ensure login warnings work correctly - with the account we just created
    # Should work and redirect to the account information page
    def test_correct_login(self):
        tester = app.test_client(self)
        response = self.app.post('/account', data={'email': 'none@none.com', 'password': 'none11'}, follow_redirects=True)
        self.assertIn(b'Account Information', response.data)

    # Test sign out
    # should redirect to log in page
    def test_sign_out(self):
        tester = app.test_client(self)
        response = self.app.post('/sign-out', follow_redirects=True)
        self.assertIn(b'Sign In', response.data)

    # Try to log in with an account that doesnt exist
    # Should not work and throw an error message
    def test_incorrect_login(self):
        tester = app.test_client(self)
        response = self.app.post('/account', data={'email': 'random@random.com', 'password': 'random'}, follow_redirects=True)
        self.assertIn(b'ERROR: Email or password not recognised', response.data)

    # Try to log into the account we just created but with the wrong passwords
    # Should not work and should tell the user that their account exists, but with a different password
    def test_correct_email_wrong_password(self):
        tester = app.test_client(self)
        response = self.app.post('/account', data={'email': 'none@none.com', 'password': 'incorrect'}, follow_redirects=True)
        self.assertIn(b'ERROR: Email recognised but password incorrect', response.data)

if __name__ == '__main__':
    unittest.main()
