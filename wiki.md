# Cruxnd Documentation

## Overview
Cruxnd-Store-API is an api for managing blogs with user authentication built on RESTful principles. 
## Setting up

Vividblog is built using [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/)and uses [Marshmallow](https://marshmallow.readthedocs.io/en/stable/) for data serialization and validation. 

1. First set up your virtual environment using a version of python. More information of how to set up a virtual environment is [here](https://www.geeksforgeeks.org/create-virtual-environment-using-venv-python/)

```bash
python3 -m venv .venv
```

2. Then install all required dependancies in the `requirements.txt` file in the root directory

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with the following parameters

| Parameters                  | Explanation                               | Possible Arguments                                  |
| --------------------------- | ----------------------------------------- | --------------------------------------------------- |
| `SECRET_KEY`                | Application secret key for extra security | Should be a random hash                             |
| `FLASK_CONFIG`              | Flask configuration                       | `default`                                           |
| `SERVER_URL`                | Server url                                | `127.0.0.1:5000/v1`                                 |
| `DEV_DATABASE_URI`          | Postgres Development Database             | `postgresql://username:password@host:port/database` |
| `TESTING_DATABASE_URI`      | Postgres Testing Database                 | `postgresql://username:password@host:port/database` |
| `DEV_DATABASE_HOST`         | Postgres Database host                    | Defaults to `127.0.0.1`                             |
| `DEV_DATABASE_PORT`         | Postgres Database port                    | Defaults to `5432`                                  |
| `DEV_DATABASE_USERNAME`     | Postgres database username                | type `SELECT user;` in your Postgres shell          |
| `DEV_DATABASE_PASSWORD`     | Postgres database password                | your database password                              |
| `DEV_DATABASE`              | Postgres database name                    | the database name                                   |
| `DEV_CACHE_TYPE`            | Possible servers for caching              | `RedisCache`                                        |
| `CACHE_REDIS_HOST`          | Server to host redis                      | `127.0.0.1`                                         |
| `CACHE_REDIS_PORT`          | Port to connect to redis                  | `6000` _5432 already taken_                         |
| `DEV_CACHE_DEFAULT_TIMEOUT` | Timeout for the cache in seconds          | defaults to one hour (_3600s_)                      |

A perfect example of the `.env` file is as follows

```ini
#* App configuration
SECRET_KEY=<secret_key>
FLASK_CONFIG=default
SERVER_URL=127.0.0.1:5000/v1

#* Database Configuration
DEV_DATABASE_URI=postgresql://username:password@127.0.0.1:5432/cruxnd-store
TESTING_DATABASE_URI=postgresql://username:password@127.0.0.1:5432/cruxnd-test

# ! Dev database parameters seperated for psycopg2
DEV_DATABASE_USER=username
DEV_DATABASE_PASSWORD=password
DEV_DATABASE_HOST=127.0.0.1
DEV_DATABASE_PORT=5432
DEV_DATABASE=cruxnd-store

#* Cache Configuration
DEV_CACHE_TYPE=RedisCache
CACHE_REDIS_HOST=127.0.0.1
CACHE_REDIS_PORT=6000
DEV_CACHE_DEFAULT_TIMEOUT=30
TESTING_CACHE_TYPE=SimpleCache
TESTING_CACHE_DEFAULT_TIMEOUT=15
```

You can generate random hashes [here](https://onlinehashtools.com/generate-random-md5-hash)

4. Run the app

```bash
./auto/boot.bat # Windows
./auto/boot.sh #Linux/MacOS
```

---

## Responses

The following are the types of responses to be expected from this API

### 404

Returned when a requested resource is not found

```json
{
	"message": "Not found"
}
```

### 204

Returned when an operation is successful.

```json
{
	"message" : "Operation Successful"
}
```

### 400

Returned when there is a wrong JSON request payload

```json
{
	"message" : "Response dict"
}
```

---
## Endpoints

The following are the endpoints that exists on the api

An endpoint communicates two things

1. The Request Payload - Data sent from the client to the server
2. The Response Payload - Data sent from the server to the client

## User Endpoints

| Endpoints            | Available Methods | Description                   |
| -------------------- | ----------------- | ----------------------------- |
| `/v1/users`          | POST, GET         | Deals with a list of users    |
| `/v1/users/<userid>` | GET, PUT, DELETE  | Deals with an individual user |

### `/v1/users`

#### POST

__Description__: Create a new User

__Request__: 

```json
{
    "username" : "Damilola",
    "email_address" : "dami@hello.com",
    "password" : "12345678",
    "age" : 45,
    "gender" : "Male"
}
```

__Response__

```json
{
  "message": "Operation Successful"
}
```

#### GET

__Description__: Get all users

__Query Parameters__:
-  __currentPage__: The current page of the response
- __itemsPerPage__:  The number of items in a particular page
- __username__: Search by username
- __emailAddress__: Search by Email Address

__Request__: 

```json
null
```

__Response__

```json
{
  "users": [
    {
      "username": "Michelle",
      "email_address": "mendozajames@example.net",
      "age": 21,
      "gender": "Male",
      "id": "7e54fe9a-3110-47ee-b570-b13c65616f6c",
      "created": "2014-11-30T00:00:00"
    },
    {
      "username": "Jacob",
      "email_address": "colonbilly@example.net",
      "age": 27,
      "gender": "Female",
      "id": "8eef9659-46fc-4dc7-a6a9-87adbcd0cd86",
      "created": "2022-03-22T00:00:00"
    }
  ],
  "current_page": 1,
  "no of pages": 63
}
```


### `v1/users/<userid>
`
#### GET

__Description__: Get a Single user

__Request__: 

```json
null
```

__Response__

```json
{
  "user": {
    "username": "Michelle",
    "email_address": "mendozajames@example.net",
    "age": 21,
    "gender": "Male",
    "id": "7e54fe9a-3110-47ee-b570-b13c65616f6c",
    "created": "2014-11-30T00:00:00"
}
```

#### PUT (auth_required)

__Description__: Update a user's Information

__Request__: 

```json
{
    "username" : "Damilola",
    "email_address" : "dami@hello.com",
    "password" : "12345678",
    "age" : 45,
    "gender" : "Male"
}
```

__Response__

```json
null
```

#### DELETE (auth_required)

__Description__: Delete a particular user

__Request__: 

```json
null
```

__Response__

```json
{
  "message": "Operation Successful"
}
```

## Product Endpoints

| Endpoint                   | Available Methods      | Description          |
| -------------------------- | ---------------------- | -------------------- |
| `/v1/products`             | GET, PUT               | A list of products   |
| `/v1/products/<productid>` | POST, GET, PUT, DELETE | A particular product |

### `/v1/products` 

#### POST (auth required)

__Description__: Add a product

__Request__:

```json
{
"name" : "Shampo 500x Plus",
"price" : "8000"
} 
```

#### GET

__Description__: Get all products
__Query Parameters__: 
-  __currentPage__: The current page of the response
- __itemsPerPage__:  The number of items in a particular page
- __name__: Search query by product name
- __min__: Filter minimum price
- __max__: Filter maximum price
- __isBought__: (_bool_ ) filter bought products

__Request__:

```json
null
```

__Response__:

```json
{
  "products": [
    {
      "name": "Oil - Canola\n",
      "price": 31000.0,
      "id": "40405d6d-6712-4561-9ee5-f041fc027711",
      "created": "2005-02-10T03:27:02",
      "updated": null,
      "is_bought": false,
      "buyer": null,
      "url": "127.0.0.1:5000/v1/products/40405d6d-6712-4561-9ee5-f041fc027711"
    },
    {
      "name": "Tuna - Canned, Flaked, Light\n",
      "price": 31000.0,
      "id": "7cf5889d-54a6-44a5-bb37-a111090548de",
      "created": "2001-11-20T01:57:43",
      "updated": null,
      "is_bought": false,
      "buyer": null,
      "url": "127.0.0.1:5000/v1/products/7cf5889d-54a6-44a5-bb37-a111090548de"
    }
  ],
  "current_page": 1,
  "no of pages": 25
}
```

#### POST

__Description__:  Add a new product.

__Request__:

```json
{
  "name" : "A new Product",
  "price" : 3000.60,
  "seller" : "f4e85be2-7e7d-42ec-858a-9dce99f63b4a"
}
```

__Response__:

```json
null
```

### `/products/<productid>`

#### GET

__Description:__ Get a particular product

__Request__:

```json
null
```

__Response__:

```json
{
  "product": {
    "name": "A new Product",
    "price": 3000.6,
    "seller": "f4e85be2-7e7d-42ec-858a-9dce99f63b4a",
    "id": "53e83149-46a0-4dc8-aff0-9a6e1135e52b",
    "created": "2024-09-25T05:58:57.625312",
    "updated": null,
    "is_bought": false,
    "buyer": null,
    "url": "127.0.0.1:5000/v1/products/53e83149-46a0-4dc8-aff0-9a6e1135e52b"
  }
}
```

#### PUT

__Description__: Update the information of a particular product

__Request__:

```json
{
  "name" : "A new Product with an updated name",
  "price" : 3000.60,
  "seller" : "9843eeb7-d027-4a6c-8364-ea54425a9fe2 "
}
```

__Response__;

```json
null
```

#### POST

__Description:__ Buys a product

__Query Parameters__
- __buyerid__: contains the buyer id that is purchasing the product

__Request__:

```json
null
```

__Response__:

```json
null
```

#### DELETE (_auth required_)

__Description:__ Delete a particular product


__Query Parameters__:
- __sellerid__: `id` of the seller deleting the product

__Request__:

```json
null
```

__Response__:

```json
null
```

## Seller Endpoints

### `/v1/sellers`

#### GET

__Description__: Get all the info for a particular user

__Request__

```json
null
```

__Response__:

```json
  {
  "sellers" :
  {
      "username": "Claire",
      "email_address": "monica83@example.com",
      "age": 39,
      "gender": "Male",
      "id": "9843eeb7-d027-4a6c-8364-ea54425a9fe2",
      "created": "2024-09-24T21:43:53.386807",
      "products": []
    },
    }
```

### `/v1/sellers/<sellerid>`

#### GET

__Description__: Get a particular seller

__Request__

```json
null
```

__Response__

```json
{
  "seller": {
    "username": "Claire",
    "email_address": "monica83@example.com",
    "age": 39,
    "gender": "Male",
    "id": "9843eeb7-d027-4a6c-8364-ea54425a9fe2",
    "created": "2024-09-24T21:43:53.386807",
    "products": []
  }
}
```

#### DELETE

__Description:__ Delete a particular seller

__Request:__

```json
null
```

__Response__:

```json
null
```
