### Login
URL: `/auth/login/`

Method: `POST`

Request Body:
```
{
    string "email": "email",
    string "password": "password"
}
```

Response:
```
{
    "status": "success",
    "message": "Login is successful.",
    "auth_token": {auth_token},
}
```