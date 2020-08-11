## Installation

1. Create virtualenv
2. Goto the project root directory and run `pip install -r requirements.txt`
3. run `python manage.py migrate`
4. Visit `http://127.0.0.1:8000/graphql/` and start playing with GraphQL!


### Some examples

### Query

- Get list of poll questions

```json
query {
  questions {
    id,
    questionText,
    pubDate
  }
}
```

- Get list of poll questions with choice(s)

```json
query {
  questions {
    id,
    questionText,
    pubDate,
    choices {
      id,
      choiceText
    }
  }
}
```

### Mutation
- Create a poll question

```json
mutation {
  createQuestion(
    questionText: "What is GraphQL?",
    pubDate: "2019-01-01T00:00:00"
  ) {
    question {
      id,
      questionText,
      pubDate
    }
  }
}
```

- Update a specific poll question

```json
mutation {
  updateQuestion(
    id: 1,
  	questionText: "My poll question"
  ) {
    question {
      id,
      questionText,
      pubDate
    }
  }
}
```

- Delete a specific poll question

```json
mutation {
  deleteQuestion(
    id: 1,
  ) {
    message
  }
}
```