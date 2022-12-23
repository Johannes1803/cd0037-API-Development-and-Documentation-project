import os
import random
import logging

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import Category, Question, setup_db

QUESTIONS_PER_PAGE = 10


def paginate(collection_, elements_per_page, page):
    start_index = elements_per_page * (page - 1)
    end_index = start_index + elements_per_page
    return collection_[start_index:end_index]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route("/categories")
    def get_categories():
        categories = Category.query.all()
        formatted_categories = {category.id: category.type for category in categories}
        return jsonify(
            {
                "success": True,
                "categories": formatted_categories,
                "total_categories": len(formatted_categories),
            }
        )

    @app.route("/questions")
    def get_questions():
        page = request.args.get("page", 1, type=int)

        categories = Category.query.all()
        formatted_categories = {category.id: category.type for category in categories}

        questions = Question.query.all()
        selected_questions = paginate(
            questions, elements_per_page=QUESTIONS_PER_PAGE, page=page
        )
        if not selected_questions:
            abort(404)
        formatted_questions = [question.format() for question in selected_questions]

        return jsonify(
            {
                "success": True,
                "questions": formatted_questions,
                "total_questions": len(questions),
                "categories": formatted_categories,
                "current_category": None,
            }
        )

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        page = request.args.get("page", 1, type=int)
        with app.app_context():
            question = Question.query.get(question_id)
            if not question:
                abort(404)
            else:
                try:
                    question.delete()
                    all_questions = question.query.all()
                    selected_questions = paginate(
                        all_questions, page=page, elements_per_page=QUESTIONS_PER_PAGE
                    )
                    formatted_questions = [
                        question.format() for question in selected_questions
                    ]
                except Exception as e:
                    app.logger.warning(e)
                    abort(500)
                else:
                    return jsonify(
                        {
                            "success": True,
                            "deleted": question_id,
                            "total_questions": len(all_questions),
                            "questions": formatted_questions,
                        }
                    )

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    return app
