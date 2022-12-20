import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        test_config = {
            "SQLALCHEMY_DATABASE_URI": "postgresql://student:student@localhost:5432/trivia_test",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        }
        self.app = create_app(test_config)
        setup_db(self.app)
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get("/categories")

        self.assertEqual(200, res.status_code)
        self.assertTrue(
            "success" in res.json
            and "categories" in res.json
            and "total_categories" in res.json
        )
        self.assertTrue(res.json["success"])
        self.assertTrue(res.json["categories"])
        self.assertTrue(res.json["total_categories"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
