# whattoread-backend
Backend HTTP API application for Books recommendation service "What To Read?"

- API
| Endpoint               | HTTP Verb         | Description                                                  |
| ---------------------- | ----------------- | ------------------------------------------------------------ |
| /ping                  | GET               | returns "pong"                                               |
| /search                | GET               | run NER model with <code>user_input</code>, output piped to Elasticsearch as filters. return list of books |
| /book_detail/{book_id} | GET               | return book meta data from Elasticsearch by <code>book_id</code> |
| /signup                | POST              | puts user in database <code>id</code>, <code>name</code>, <code>password</code>, <code>email</code> required. |
| /login                 | POST              | returns jwt token                                            |
| /bookshelf             | POST, DELETE, GET | PUT : save book_id to user shelf <br>DELETE : delete book_id from user shelf <br>GET : return book_id list for user |

- url for application : http://13.209.42.183:5000

- /signup example


```
// request
Content-Type: application/json

{
"id" : "sangmin",
"name" : "simon",
"password" : "1234",
"email" : "sangmin@email.com"
}

// response
// if email duplicate
email sangmin@email.com is already in use
// if id duplicate
user sangmin already exists
// on success
successfully created user sangmin
```


- /login example

```
// request
Content-Type: application/json

{
"id": "sangmin",
"password": "1234"
}

// response
{"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoic2FuZ20xaW4iLCJleHAiOjE2MjIyMzI0NTN9.hIEQeWs70rBH7CToraJhTSzDDcsUMaNwEg6iwDVKhYw","user_id":"sangmin"}
```

- /bookshelf example

```
// POST request
Content-Type: application/json
Authorization : <access_token>

{
"book_id" : <book_id>
}
// response
// if book already exist
book_id <book_id> already exists in sangmin bookshelf
// on success
book_id <book_id> put to sangmin bookshelf


// DELETE request
Content-Type: application/json
Authorization : <access_token>

{
"book_id" : <book_id>
}
// response
book_id <book_id> deleted from sangmin bookshelf


// GET request
Authorization : <access_token>
// response
[<book_id>, <book_id>, ...]
```

