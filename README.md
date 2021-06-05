# whattoread-backend
> Backend HTTP API application for Books recommendation service "What To Read?"

- whattoread-frontend : https://github.com/JiWM/BookSearch


## 📅 Project Schedule
- 2021/05/13 ~ 2021/06/08 

## ⭐ Software Stack
- Web Application Frameworkd : Flask(Layered architecture)
- Database : Elasticsearch
- Web Scraping : Selenium, Beautifulsoup

## API
![image](https://user-images.githubusercontent.com/68796085/120313846-83544680-c315-11eb-9cd1-4dd774bc669e.png)


- /search example

```
// request
/search?user_input=user input string

// response
{"_shards":{"failed":0,"skipped":0,"successful":1,"total":1},"hits":{"hits":[{"_id":"73","_index":"book","_score":6.8311615,"_source":{"author":"Beatrix Potter","avg_rating":4.1,"genre":["Childrens","Classics","Childrens","Picture Books","Fiction","Animals","Fantasy","Childrens","Juvenile","Kids","Young Adult","Childrens","Childrens Classics"],"publish_date":"1960","title":"Rabbit"},"_type":"_doc"},{"_id":"14","_index":"book","_score":5.2149377,"_source":{"author":"Cormac McCarthy","avg_rating":4.0,"genre":["Fiction","Historical","Historical Fiction","Westerns","Classics","Literature","Novels","Literature","American","Horror","Historical","Literary Fiction"],"publish_date":"1986","title":"Blood Meridian"},"_type":"_doc"},
...
...
```

- /book_detail example

```
// request
/book_detail/1

// response
{"_shards":{"failed":0,"skipped":0,"successful":1,"total":1},"hits":{"hits":[{"_id":"1","_index":"book","_score":1.0,"_source":{"author":"Robert Penn Warren","avg_rating":4.2,"description":"More than just a classic political novel, Warren\u2019s tale of power and corruption in the Depression-era South is a sustained meditation on the unforeseen consequences of every human act, the vexing connectedness of all people and the possibility\u2014it\u2019s not much of one\u2014of goodness in a sinful world. Willie Stark, Warren\u2019s lightly disguised version of Huey Long, the one time Louisiana strongman/governor, begins as a genuine tribune of the people and ends as a murderous populist demagogue. Jack Burden is his press agent, who carries out the boss\u2019s orders, first without objection, then in the face of his own increasingly troubled conscience. And the politics? For Warren, that\u2019s simply the arena most likely to prove that man is a fallen creature. Which it does.","genre":["Fiction","Classics","Historical","Historical Fiction","Politics","Literature","Novels","Literature","American","Literary Fiction","American","Southern","Historical"],"publish_date":"1946","title":"All the King\u2019s Men"},"_type":"_doc"}],"max_score":1.0,"total":{"relation":"eq","value":1}},"timed_out":false,"took":19}

```


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

