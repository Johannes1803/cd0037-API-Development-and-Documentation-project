# API Documentation

## Endpoints

### Get categories

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: A json object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

Example response:
```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

### Get questions

`GET /api/v1.0/questions'`

- Get the questions of the trivia api. Results are paginated.
- Request Arguments:
    - page: optional[int] - which page of the results to return, defaults to 1
- Returns:
    a json object with the following keys:
    - success: boolean status 
    - questions: list of questions, where each question is an object with question, answer, category and difficulty key.
    - total_questions: number of total_questions in the trivia api
    - current_category: category of current question

Example response:
```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        ...,    
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        }
    ],
    "success": true,
    "total_questions": 22
}
```

### Delete a particular question

`DELETE '/api/v1.0/questions/<int:question_id>'`

- Delete the question specified by question_id in the route.
- Request Arguments:
    - page: optional[int] - which page of the results to return, defaults to 1

- Returns:
    a json object with the following keys:
    - success: boolean status 
    - deleted: id of deletetd question
    - total_questions: number of total questions in api after deletion
    - questions: list of questions, where each question is an object with question, answer, category and difficulty key.


### Post a new question

`POST '/api/v1.0/questions/'`
 
 - Post a new question.
 - Request Arguments: None
 - Request body: json object representation of a question with keys 'question', 'answer', 'category', 'difficulty'
 - Returns:
    a json object with the following keys:
    - success: boolean status 
    - total_questions: number of total questions in api after deletion
    - questions: list of questions, where each question is an object with question, answer, category and difficulty key.
    - created: id of created question

Example request body:
```json
{    
    "question": "Who was the second James Bond?",
    "answer": "Roger Moore",
    "category": 3,
    "difficulty": 2
}
```

Example Response:
```json
{
    "created": 33,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        ...
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        }
    ],
    "success": true,
    "total_questions": 23
}
```

### Search a question

`POST '/api/v1.0/questions/'`

- Search a question by search_term. Results are paginated.
- Request Arguments:
    - page: optional[int] - which page of the results to return, defaults to 1
- Request body: json object with key 'searchTerm'
- Returns:
    a json object with the following keys:
    - success: boolean status 
    - questions: list of questions, where each question is an object with question, answer, category and difficulty key. **Can be a list with zero elements**, if no matches were found for the search term.
    - total_questions: number of total_questions matching the search term.

### Get questions of one category

`GET '/api/v1.0/categories/<int:category_id>/questions'`

- Get questions of one category. Results are paginated.
- Request Arguments:
    - page: optional[int] - which page of the results to return, defaults to 1
- Returns:
    a json object with the following keys:
    - success: boolean status 
    - questions: list of questions, where each question is an object with question, answer, category and difficulty key. All questions share the same category as defined in the route.
    - total_questions: number of total_questions within the category.

### Get next question in quiz mode

`POST '/api/v1.0/quizzes'`

- Get an unasked question from a specific category.
- Request Arguments: None
- Request body: 
    - json object with key 'previous_questions' and 'quiz_category'.
- Returns:
    a json object with the following keys:
    - success: boolean status 
    - question:  object with question, answer, category and difficulty key.

Example request body:
```json
{
    "quiz_category": {"id": 1, "type": "science"},
    "previous_questions": [1, 3, 7, 20, 40, 22, 25]
}
```

Example response:
```json
{
    "question": {
        "answer": "Albert Einstein",
        "category": 1,
        "difficulty": 1,
        "id": 26,
        "question": "Who invented the relativity theory?"
    },
    "success": true
}
```


