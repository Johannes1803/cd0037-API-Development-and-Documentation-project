import random

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
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
        formatted_categories = {
            category.id: category.type for category in categories
        }
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
        formatted_categories = {
            category.id: category.type for category in categories
        }

        questions = Question.query.all()
        selected_questions = paginate(
            questions, elements_per_page=QUESTIONS_PER_PAGE, page=page
        )
        if not selected_questions:
            abort(404)
        formatted_questions = [
            question.format() for question in selected_questions
        ]

        # get string rep of first question's category
        try:
            cat_id = formatted_questions[0]["category"]
            cat_name = formatted_categories[cat_id]
        except KeyError as e:
            app.logger.debug(e)
            abort(500)
        else:
            return jsonify(
                {
                    "success": True,
                    "questions": formatted_questions,
                    "total_questions": len(questions),
                    "categories": formatted_categories,
                    "current_category": cat_name,
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
                        all_questions,
                        page=page,
                        elements_per_page=QUESTIONS_PER_PAGE,
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

    @app.route("/questions", methods=["POST"])
    def post_new_question():
        """Post a new question."""
        page = request.args.get("page", 1, type=int)

        if request.json.get("searchTerm"):
            with app.app_context():
                categories = Category.query.all()
                formatted_categories = {
                    category.id: category.type for category in categories
                }

                search_term = request.json["searchTerm"].lower()
                all_matching_questions = Question.query.filter(
                    Question.question.ilike("%{}%".format(search_term))
                ).all()
                current_matching_questions = paginate(
                    all_matching_questions,
                    elements_per_page=QUESTIONS_PER_PAGE,
                    page=page,
                )
                current_matching_questions = [
                    question.format()
                    for question in current_matching_questions
                ]
                if not current_matching_questions:
                    return jsonify(
                        {
                            "success": True,
                            "questions": current_matching_questions,
                            "total_questions": len(all_matching_questions),
                            "current_category": None,
                        }
                    )
                else:
                    try:
                        cat_id = current_matching_questions[0]["category"]
                        cat_name = formatted_categories[cat_id]

                    except KeyError as e:
                        app.logger.debug(e)
                        abort(500)
                    return jsonify(
                        {
                            "success": True,
                            "questions": current_matching_questions,
                            "total_questions": len(all_matching_questions),
                            "current_category": cat_name,
                        }
                    )

        else:
            with app.app_context():
                try:
                    question = Question(
                        question=request.json["question"],
                        answer=request.json["answer"],
                        category=request.json["category"],
                        difficulty=request.json["difficulty"],
                    )
                except KeyError as e:
                    app.logger.warning(e)
                    abort(422)

                else:
                    try:
                        question.insert()

                        all_questions = Question.query.all()
                        current_questions = paginate(
                            all_questions,
                            elements_per_page=QUESTIONS_PER_PAGE,
                            page=page,
                        )
                        current_questions = [
                            question.format() for question in current_questions
                        ]
                    except Exception as e:
                        app.logger.debug(e)
                        abort(500)
                    else:
                        return jsonify(
                            {
                                "success": True,
                                "questions": current_questions,
                                "total_questions": len(all_questions),
                                "created": question.id,
                            }
                        )

    @app.route("/categories/<int:category_id>/questions")
    def get_category(category_id):
        page = request.args.get("page", 1, type=int)

        category = Category.query.get(category_id)
        if not category:
            abort(404)
        else:
            questions_of_category = Question.query.filter(
                Question.category == category.id
            ).all()
            current_questions_of_category = paginate(
                questions_of_category,
                elements_per_page=QUESTIONS_PER_PAGE,
                page=page,
            )
            current_questions_of_category = [
                question.format() for question in current_questions_of_category
            ]
            return jsonify(
                {
                    "success": True,
                    "questions": current_questions_of_category,
                    "total_questions": len(questions_of_category),
                    "current_category": category.type,
                }
            )

    @app.route("/quizzes", methods=["POST"])
    def get_quiz_question():
        try:
            app.logger.debug(request.json)
            previous_questions = request.json["previous_questions"]
            quiz_category_id = request.json.get("quiz_category", {}).get("id")
        except KeyError as e:
            app.logger.warning(e)
            abort(422)
        else:
            try:
                if quiz_category_id:
                    questions = Question.query.filter(
                        Question.category == quiz_category_id,
                        ~Question.id.in_(previous_questions),
                    ).all()
                else:
                    questions = Question.query.filter(
                        ~Question.id.in_(previous_questions),
                    ).all()
            except Exception as e:
                app.logger.warning(e)
                abort(500)
            else:
                resp_dict = {
                    "success": True,
                }
                question = (
                    random.choice(questions).format() if questions else None
                )
                if question:
                    resp_dict["question"] = question
                return jsonify(resp_dict)

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 404,
                    "message": "resource not found",
                }
            ),
            404,
        )

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 422,
                    "message": "Unprocessable Entity",
                }
            ),
            422,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 500,
                    "message": "Internal Server Error",
                }
            ),
            500,
        )

    return app
