### Create new user
URL: `/users/`

Method: `POST`

Request Body:
```
{
    string "email": "email",
    string "password": "password",
    string "bio": "bio"
}
```

Response:
```
{
    "status": "success",
    "message": "User with email {email} has been created successfully.",
    "id": {new_user_id} 
}
```

### Get User
URL: `/users/{user_id}/`

Method: `GET`

Headers: Authorization = Bearer + JWT token

Response:
```
{
    "status": "success",
    "message": "User have been retrieved successfully.",
    "user": {
        "id": {user_id},
        "email": "alexfurm@mail.com",
        "bio": "bio",
        "created_at": "31.07.2021",
        "updated_at": "10.08.2021"
    }
}
```

### Get All Users
URL: `/users/`

Method: `GET`

Headers: Authorization = Bearer + JWT token

Response:
```
{
    "status": "success",
    "message": "Users have been listed successfully.",
    "users": [
        {
            "id": {user_id},
            "email": "alexfurm@mail.ru",
            "bio": "my bio",
            "created_at": "15.07.2021",
            "updated_at": "25.07.2021"
        },
        {
            "id": {user_id},
            "email": "alex@mail.com",
            "bio": "bio",
            "created_at": "30.07.2021",
            "updated_at": "31.07.2021"
        },
        {
            "id": {user_id},
            "email": "alexfurm@mail.com",
            "bio": "bio",
            "created_at": "31.07.2021",
            "updated_at": "25.08.2021"
        }
    ]
}
```

### Update a user
URL: `/users/{user_id}/`

Method: `PUT`

Headers: Authorization = Bearer + JWT token

Request Body:
```
{
    string "bio": "bio"
}
```

Response:
```
{
    "status": "success",
    "message": "User with id {user_id} has been updated successfully."
}
```


### Delete a user
URL: `/users/{user_id}/`

Method: `DELETE`

Headers: Authorization = Bearer + JWT token

Response:
```
{
    "status": "success",
    "message": "User with id {user_id} has been deleted successfully."
}
```