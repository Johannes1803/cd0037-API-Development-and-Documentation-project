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

    def test_get_categories_should_return_results(self):
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

    def test_get_questions_should_return_results(self):
        """Test get request to '/questions' route returns results in expected format"""
        res = self.client().get("/questions?page=2")

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
        res = self.client().get("/questions?page=1000")

        self.assertEqual(404, res.status_code)
        self.assertTrue("success" in res.json and "error" in res.json)
        self.assertFalse(res.json["success"])

    def test_delete_question_should_remove_db_entry(self):
        """Making a delete request should remove question from db"""
        # check question is in db before request
        question_id = 5
        with self.app.app_context():
            question = Question.query.get(question_id)
            self.assertTrue(question)

        # make DELETE request
        res = self.client().delete(f"/questions/{question_id}")

        # check response
        self.assertEqual(200, res.status_code)
        self.assertTrue(res.json["success"])
        self.assertEqual(question_id, res.json["deleted"])
        self.assertTrue(res.json["total_questions"])
        self.assertTrue(len(res.json["questions"]))

        # check entry is removed from db
        with self.app.app_context():
            question = Question.query.get(question_id)
            self.assertIsNone(question)

    def test_delete_question_should_raise_404(self):
        """Trying to delete a question that does not exist should raise a 404 error."""
        # make DELETE request
        res = self.client().delete("/questions/100000")

        # check response
        self.assertEqual(404, res.status_code)
        self.assertTrue("success" in res.json and "error" in res.json)
        self.assertFalse(res.json["success"])

    def test_post_new_question_should_return_id_of_created_item(self):
        """Posting a new question should return success response."""
        # make POST request
        res = self.client().post(
            "/questions",
            json={
                "question": "Who was the second James Bond Actor?",
                "answer": "Roger Moore",
                "category": 3,
                "difficulty": 3,
            },
        )

        self.assertEqual(200, res.status_code)
        self.assertTrue(
            "success" in res.json
            and "created" in res.json
            and "total_questions" in res.json
        )

    def test_post_new_question_missing_arg_should_return_422(self):
        """Forgetting a required arg to init a new question should raise a 422 error."""
        # make POST request
        res = self.client().post(
            "/questions",
            json={
                "answer": "Roger Moore",
                "category": 3,
                "difficulty": 3,
            },
        )

        self.assertEqual(422, res.status_code)
        self.assertTrue("success" in res.json and "error" in res.json)
        self.assertFalse(res.json["success"])

    def test_search_question_should_return_results(self):
        """Searching a question should return results (assuming at least one match)"""
        res = self.client().post("/questions", json={"searchTerm": "title"})

        self.assertEqual(200, res.status_code)
        self.assertTrue(
            "success" in res.json
            and "questions" in res.json
            and "total_questions" in res.json
        )
        self.assertTrue(res.json["success"])
        self.assertTrue(res.json["questions"])
        self.assertTrue(res.json["total_questions"])

    def test_search_question_no_match_should_return_empty_list(self):
        """Empty list should be returned assuming search term with zero matches."""
        res = self.client().post("/questions", json={"searchTerm": "qqqas"})

        self.assertEqual(200, res.status_code)
        self.assertTrue(
            "success" in res.json
            and "questions" in res.json
            and "total_questions" in res.json
        )
        self.assertTrue(res.json["success"])
        self.assertFalse(res.json["questions"])
        self.assertEqual(0, res.json["total_questions"])

    def test_get_questions_of_category_should_return_results(self):
        """Sending GET request to '/categories/<id>/questions' should return results."""
        res = self.client().get("/categories/1/questions")

        self.assertEqual(200, res.status_code)
        self.assertTrue(
            "success" in res.json
            and "questions" in res.json
            and "total_questions" in res.json
        )
        self.assertTrue(res.json["success"])
        self.assertTrue(res.json["questions"])
        self.assertTrue(res.json["total_questions"])

    def test_get_questions_of_category_should_return_404(self):
        """Sending GET request to '/categories/<id>/questions' should return 404 if category does not exist."""
        res = self.client().get("/categories/10000/questions")

        # check response
        self.assertEqual(404, res.status_code)
        self.assertTrue("success" in res.json and "error" in res.json)
        self.assertFalse(res.json["success"])

    def test_post_quizzes_should_return_random_unseen_question(self):
        """Sending POST request to '/quizzes' should return a new, unseen question."""
        previous_questions = [1, 3, 7, 20, 40]
        res = self.client().post(
            "/quizzes", json={"previous_questions": previous_questions, "category": 1}
        )

        # check responses
        self.assertEqual(200, res.status_code)
        self.assertTrue("success" in res.json and "question" in res.json)
        self.assertTrue(res.json["success"])
        self.assertTrue(res.json["question"])
        self.assertFalse(res.json["question"].id in previous_questions)

    def test_post_quizzes_should_return_422_missing_keys_in_body(self):
        """Sending POST request to '/quizzes' should return a 422 error if required key in body is missing."""
        res = self.client().post(
            "/quizzes", json={"previous_questions": [1, 3, 7, 20, 40]}
        )

        # check responses
        self.assertEqual(422, res.status_code)
        self.assertTrue("success" in res.json and "error" in res.json)
        self.assertFalse(res.json["success"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
