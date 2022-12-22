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
            "TESTING": True,
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

    def test_get_categories_should_return_json(self):
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

    def test_get_categories_should_raise_404(self):
        """If pagination exceeds number of available pages, return 404."""
        res = self.client().get("/categories?page=1000")

        self.assertEqual(404, res.status_code)
        self.assertTrue("success" in res.json and "error" in res.json)

    def test_get_questions_should_return_json(self):
        """Test get request to '/questions' route returns results in expected format"""
        res = self.client().get("/questions?page=3")

        self.assertEqual(200, res.status_code)
        self.assertTrue(
            "success" in res.json
            and "questions" in res.json
            and "total_questions" in res.json
        )
        self.assertTrue(res.json["success"])
        self.assertTrue(res.json["questions"])
        self.assertTrue(res.json["total_questions"])

    def test_get_questions_should_raise_404(self):
        """If pagination exceeds number of available pages, return 404."""
        res = self.client().get("/pages?page=1000")

        self.assertEqual(404, res.status_code)
        self.assertTrue("success" in res.json and "error" in res.json)
        self.assertFalse(res.json["success"])

    def test_delete_question_should_remove_db_entry(self):
        """Making a delete request should remove question from db"""
        # check question is in db before request
        with self.app.app_context():
            question = Question.query.get(1)
            self.assertTrue(question)

        # make DELETE request
        res = self.client().delete("/questions/1")

        # check response
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res["success"], True)
        self.assertEqual(res["deleted"], 2)
        self.assertTrue(res["total_questions"])
        self.assertTrue(len(res["questions"]))

        # check entry is removed from db
        with self.app.app_context():
            question = Question.query.get(1)
            self.assertIsNone(question)

    def test_delete_question_should_raise_404(self):
        """Trying to delete a question that does not exist should raise a 404 error."""
        # make DELETE request
        res = self.client().delete("/questions/100000")

        # check response
        self.assertEqual(404, res.status_code)
        self.assertTrue("success" in res.json and "error" in res.json)
        self.assertFalse(res.json["success"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
