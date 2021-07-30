# Full example

## Overview
For resolver the test I developed the endpoints:

| Code                                                    | Description                                           |
|---------------------------------------------------------|-------------------------------------------------------|
| /login                                                  | To Authenticate on application.                       |
| /users                                                  | To create users on application.                       |
| /users/{user_id}/galleries                              | Your login or password don't match                    |
| /galleries                                              | Show the user galleries.                              |
| /galleries/{galleries_id}/friend                        | Show your galleries.                                  |
| /galleries/{galleries_id}/approver                      | Add a user for send new photos.                       |
| /galleries/{galleries_id}/pictures                      | Add permissions for another users approve new photos. |
| /galleries/{galleries_id}/pictures/{picture_id}/like    | Show and save images from a gallery.                  |
| /galleries/{galleries_id}/pictures/{picture_id}/approve | Approve a photo.                                      |

## Authentication
Some endpoints needed authentication. This project user JWT bearer token in the header to validate a logged user. If you do successfull login, the responde will be:

```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyNzYwNDkzNCwianRpIjoiMjM4Nzc1ODYtZTUyZC00NmExLWFmNjAtOTg2NWFjYTY3ZGY5IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiZW1haWwiOiJoYW5kNkBnbWFpbC5jb20iLCJpZCI6IjYwZmMyMzU5NTBjZWNmOWNjZjY0MWE0MiJ9LCJuYmYiOjE2Mjc2MDQ5MzQsImV4cCI6MTYzMDE5NjkzNH0.RGgBavDQbtG8JBAHGEuzUkUtkfjRHlk_vlU40ABamV0",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyNzYwNDkzNCwianRpIjoiMTg0ODY4ZjctMTcyYy00ZDJkLWI1MzQtN2M5MWUzZjFlODk2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJlbWFpbCI6ImhhbmQ2QGdtYWlsLmNvbSIsImlkIjoiNjBmYzIzNTk1MGNlY2Y5Y2NmNjQxYTQyIn0sIm5iZiI6MTYyNzYwNDkzNCwiZXhwIjoxNjI3NjEyMTM0fQ.8SEW-cIIEdY6wnLqqcBWCcAnEfkHEOF_bKjnIegAigM"
}
```

The **access_token** permits you to access protected resources and identify with the user do the request. By default, your expiration was set at 120 min.

The **refresh_token** permits you to request a new valid access token in case your access token was expired.

## Login

### /login
Endpoint to validate a email and passord from a user, responding with access token.

- POST

**Payload:**

| Field                 | Type  | Required | Descripton            |
|-----------------------|-------|----------|-----------------------|
| **email**             | `str` |    yes   | User Email            |
| **password**          | `str` |    yes   | User Password         |


**Responses Code:**

| Code  | Descripton                         |
|-------|------------------------------------|
| 200   | Success                            |
| 400   | Body Validation Error              |
| 401   | Your login or password don't match |

**Example**

    curl --request POST \
    --url {{your_host}}/api/v1/login \
    --header 'Content-Type: application/json' \
    --data '{
        "email": "hand7@gmail.com",
        "password": "123345345"
    }'

**Response:**

```json
# 200 Success
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}

```


## Users

Endpoint to validate a email and passord from a user, responding with access token.

### /users
- POST

Create a new User

**Payload:**

| Field                 | Type  | Required | Description           | Valitate 
|-----------------------|-------|----------|-----------------------|--------------------|
| **email**             | `str` |    yes   | User Email            |                    |
| **password**          | `str` |    yes   | User Password         | Minimum length 8.  |
| **name**              | `str` |    yes   | User Name             |                    |


**Responses Code:**

| Code  | Description                        |
|-------|------------------------------------|
| 201   | Created                            |
| 400   | Body Validation Error              |
| 400   | User Already Exists                |

**Example**

    curl --request POST \
    --url {{your_host}}/api/v1/users \
    --header 'Content-Type: application/json' \
    --data '{
        "email": "hand8@gmail.com",
        "name": "Hand medeiros",
        "password": "123345345"
    }'

**Response:**

```json
# 201 Success
None

```

### /users/{user_id}/galleries 
- Get

See galleries from a user by your user_id

**Payload:**

| Field                 | Type  | Required | Description           | Valitate 
|-----------------------|-------|----------|-----------------------|--------------------|

**Responses Code:**

| Code  | Descripton                         |
|-------|------------------------------------|
| 200   | Success                            |
| 401   | Missing Authorization Header       |
| 404   | User not found                     |

**Example**

    curl --request GET \
    --url {{your_host}}/api/v1/users/60fc235950cecf9ccf641a42/galleries \
    --header 'Authorization: Bearer {access_token}' \
    --header 'Content-Type: application/json'

**Response:**

```json
# 200 Success
[
    {
        "id": "60fd983458915aef4be70c06",
        "created_at": "2021-07-25T16:57:42.161000",
        "name": "galery 04"
    }
]

```

## Galleries

### /galleries 
- Get

See your galleries.


**Payload:**

| Field                 | Type  | Required | Description           | Valitate 
|-----------------------|-------|----------|-----------------------|--------------------|

**Responses Code:**

| Code  | Descripton                         |
|-------|------------------------------------|
| 200   | Success                            |
| 401   | Missing Authorization Header       |

**Example**

    curl --request GET \
    --url {{your_host}}/api/v1/galleries \
    --header 'Authorization: Bearer {access_token}' \
    --header 'Content-Type: application/json'

**Response:**

```json
# 200 Success
[
  {
    "name": "galery 04 user 07",
    "id": "6102fc1bd348de0fe55b7fc0",
    "created_at": "2021-07-29T19:05:02.034000"
  }
]
```

- POST

Create a new for you

**Payload:**

| Field                 | Type  | Required | Description           | Valitate 
|-----------------------|-------|----------|-----------------------|--------------------|
| **name**              | `str` |    yes   | Gallery Name          |                    |


**Responses Code:**

| Code  | Description                        |
|-------|------------------------------------|
| 201   | Created                            |
| 400   | Body Validation Error              |
| 401   | Missing Authorization Header       |

**Example**

    curl --request POST \
    --url {{your_host}}/api/v1/galleries \
    --header 'Authorization: Bearer {access_token}' \
    --header 'Content-Type: application/json' \
    --data '{
        "name": "galery 04 user 07"
    }'

**Response:**

```json
# 201 Created
None

```

### /galleries/{galleries_id}/friend
- POST

Add a user to can upload photos to your gallery

**Payload:**

| Field                 | Type  | Required | Description                       | Valitate   |
|-----------------------|-------|----------|-----------------------------------|------------|
| **email**             | `str` |    yes   | email from an active system user  |            |


**Responses Code:**

| Code  | Description                        |
|-------|------------------------------------|
| 200   | Success                            |
| 400   | Body Validation Error              |
| 401   | Missing Authorization Header       |
| 404   | User not found                     |
| 404   | Gallery not found                  |

**Example**

    curl --request POST \
    --url {{your_host}}/api/v1/gallery/60fd983458915aef4be70c06/friend \
    --header 'Authorization: Bearer {access_token}' \
    --header 'Content-Type: application/json' \
    --data '{
        "email": "hand7@gmail.com"
    }'

**Response:**

```json
# 200 Success
None

```

### /galleries/{galleries_id}/approver
- POST

Add a user to can approve photos to show it to all users.

**Payload:**

| Field                 | Type  | Required | Description                       | Valitate   |
|-----------------------|-------|----------|-----------------------------------|------------|
| **email**             | `str` |    yes   | email from an active system user  |            |


**Responses Code:**

| Code  | Description                        |
|-------|------------------------------------|
| 200   | Success                            |
| 400   | Body Validation Error              |
| 401   | Missing Authorization Header       |
| 404   | User not found                     |
| 404   | Gallery not found                  |

**Example**

    curl --request POST \
    --url {{your_host}}/api/v1/gallery/60feeafa614ca53869b8b305/approver \
    --header 'Authorization: Bearer {access_token}' \
    --header 'Content-Type: application/json' \
    --data '{
        "email": "hanasdd5@gmail.com"
    }'

**Response:**

```json
# 200 Success
None

```

## Pictures

### /galleries/{galleries_id}/pictures
- Get 

Get the pictures from a gallery by galery_id.

You can see get all the pictures if your are gallery admin (have permission to approver). If not, you can see only pictures with **approved** status is **True**.

**Filtros disponíveis:**

- `page`: Number of page.
- `limit`: How many pictures you can per pages.

**Payload:**

| Field                 | Type  | Required | Description           | Valitate 
|-----------------------|-------|----------|-----------------------|--------------------|

**Responses Code:**

| Code  | Descripton                         |
|-------|------------------------------------|
| 200   | Success                            |
| 401   | Missing Authorization Header       |
| 404   | Gallery not found                  |

**Example**

    curl --request GET \
    --url '{{your_host}}/api/v1/gallery/60fd983458915aef4be70c06/pictures?page=0&limit=3' \
    --header 'Authorization: Bearer {access_token}' \
    --header 'Content-Type: application/json'

**Response:**

User not Admin

```json
# 200 Success
{
  "result": [
    {
      "id": "36e824e5-14c1-4bee-a194-c3a05ca78035",
      "description": "eitasdae",
      "updated_at": "2021-07-25T21:00:02.119000",
      "approved": true,
      "name": "123",
      "likes": 2,
      "url": "http://friend-gallery.s3.amazonaws.com/files/60fc235950cecf9ccf641a42/60fd983458915aef4be70c06/index1.jpeg",
      "created_at": "2021-07-25T21:00:02.119000"
    }
  ],
  "count": 11,
  "next_page": "/gallery/60fd983458915aef4be70c06/pictures?page=1&limit=3",
  "previous_page": "/gallery/60fd983458915aef4be70c06/pictures?page=0&limit=3"
}

```

User Admin

```json
# 200 Success

{
  "result": [
    {
      "name": "123",
      "url": "http://friend-gallery.s3.amazonaws.com/files/60fc235950cecf9ccf641a42/60fd983458915aef4be70c06/index1.jpeg",
      "approved": true,
      "id": "36e824e5-14c1-4bee-a194-c3a05ca78035",
      "updated_at": "2021-07-25T21:00:02.119000",
      "created_at": "2021-07-25T21:00:02.119000",
      "likes": 2,
      "description": "eitasdae"
    },
    {
      "name": "123",
      "url": "http://friend-gallery.s3.amazonaws.com/files/60fc235950cecf9ccf641a42/60fd983458915aef4be70c06/index2.jpeg",
      "approved": false,
      "id": "49020d0f-9c88-4c46-bac5-0ae9c39c2f95",
      "updated_at": "2021-07-25T21:00:26.187000",
      "created_at": "2021-07-25T21:00:26.187000",
      "likes": 0,
      "description": "eitasdae"
    },
    {
      "name": "123",
      "url": "http://friend-gallery.s3.amazonaws.com/files/60fc235950cecf9ccf641a42/60fd983458915aef4be70c06/index3.jpeg",
      "approved": false,
      "id": "615109d9-293b-42b4-820b-0bc23fc91bac",
      "updated_at": "2021-07-25T21:55:33.083000",
      "created_at": "2021-07-25T21:55:33.083000",
      "likes": 0,
      "description": "eitasdae"
    }
  ],
  "next_page": "/gallery/60fd983458915aef4be70c06/pictures?page=1&limit=3",
  "previous_page": "/gallery/60fd983458915aef4be70c06/pictures?page=0&limit=3",
  "count": 11
}
```

- POST

Create a new picture in the gallery.

**Payload:**

| Field                 | Type  | Required | Description           | Valitate 
|-----------------------|-------|----------|-----------------------|------------------------------------------------|
| **photo_file**        | `File`|    yes   | Photo File            | Accept only extensions: png, jpg, jpeg and gif |
| **name**              | `str` |    yes   | Photo Name            |                                                |
| **description**       | `str` |    no    | Photo description     |                                                |


**Responses Code:**

| Code  | Description                        |
|-------|------------------------------------|
| 201   | Created                            |
| 400   | Body Validation Error              |
| 401   | Missing Authorization Header       |
|       | You dont have permission to upload |
| 404   | Gallery not found                  |

**Example**

    curl --request POST \
    --url {{your_host}}/api/v1/gallery/60fd983458915aef4be70c06/pictures \
    --header 'Authorization: Bearer {acces_token}' \
    --header 'Content-Type: multipart/form-data; boundary=---011000010111000001101001' \
    --form photo_file=@/home/dell/Pictures/index.jpeg \
    --form 'name="123"' \
    --form 'description="asdasda"'

**Response:**

```json
# 201 Created
None

```

### /galleries/{galleries_id}/pictures/{picture_id}/like

- Post 

Like a picture.


**Payload:**

| Field                 | Type  | Required | Description           | Valitate 
|-----------------------|-------|----------|-----------------------|--------------------|

**Responses Code:**

| Code  | Descripton                                           |
|-------|------------------------------------------------------|
| 200   | Success                                              |
| 401   | Missing Authorization Header                         |
| 404   | Gallery not found                                    |
| 404   | Picture not found                                    |


### /galleries/{galleries_id}/pictures/{picture_id}/approve

- Put 

Approve a picture to show it to all users.


**Payload:**

| Field                 | Type  | Required | Description           | Valitate 
|-----------------------|-------|----------|-----------------------|--------------------|

**Responses Code:**

| Code  | Descripton                                           |
|-------|------------------------------------------------------|
| 200   | Success                                              |
| 401   | Missing Authorization Header                         |
| 401   | Don't have permission for approve this picture       |
| 404   | Gallery not found                                    |
| 404   | Picture not found                                    |

## Erros

```json
# 4xx Error Generics
{
  "message": "User Already Exists",
  "status_code": 400
}

# 400 Validation Error
{
  "field": [
    "Messages"
  ]
}

# 401 Unauthorized
{
  "msg": "Token has expired"
}
```