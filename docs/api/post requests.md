### Create new post
URL: `/posts/`

Method: `POST`

Headers: Authorization = Bearer + JWT token

Request Body:
```
{
    "post_details": {
        string "name": "post name",  
        string "description": "post description", 
        string "type": {type_id}
    },
    "address": {
        string "country": "country",  
        string "city": "city",  
        string "street": "street",  
        string "house_no": "3",  
        string "floor": "4"  
    }
}
```

The post types can be different:

`4da2d6c7-e4c8-4b7f-b621-09acaa4fda30`: educational meetup

`1ef5e908-a2c5-4561-998b-02eb5d14cb73`: sport meetup

`863f8aa0-7d99-4269-9d40-606fd6b089a3`: professional meetup

Response:
```
{
    "status": "success",
    "message": "New post has been successfully created.",
    "id": {new_post_id} 
}
```

### Get Post
URL: `/posts/{post_id}/`

Method: `GET`

Headers: Authorization = Bearer + JWT token

Response:
```
{
    "status": "success",
    "message": "Post have been retrieved successfully.",
    "post": {
        "id": {post_id},
        "user_id": {user_id},
        "address": {
            "country": "Russia",
            "city": "Kaliningrad",
            "street": "Central Square",
            "house_no": "5",
            "floor": "3"
        },
        "name": "Test Post Name",
        "description": "Test Post Description",
        "type": "Test meetup"
    }
}
```

### Get All Posts
URL: `/posts/`

Method: `GET`

Headers: Authorization = Bearer + JWT token

Response:
```
{
    "status": "success",
    "message": "Posts have been listed successfully.",
    "posts": [
        {
            "id": {post_id},
            "user_id": {user_id},
            "address": {
                "country": "Russia",
                "city": "Kaliningrad",
                "street": "Central Square",
                "house_no": "5",
                "floor": "3"
            },
            "name": "Test Post Name",
            "description": "Test Post Description",
            "type": "Test meetup"
        }
    ]
}
```

### Update a post
URL: `/posts/{post_id}/`

Method: `PUT`

Headers: Authorization = Bearer + JWT token

Request Body:
```
{
    string "name": "post name",
    string "description": "post description",
    string "type": "post type"
}
```

Response:
```
{
    "status": "success",
    "message": "Post with id {post_id} has been updated successfully."
}
```


### Update an address of a post
URL: `/posts/{post_id}/address/`

Method: `PUT`

Headers: Authorization = Bearer + JWT token

Request Body:
```
{
    string "country": "country",  
    string "city": "city",  
    string "street": "street",  
    string "house_no": "3",  
    string "floor": "4"  
}
```

Response:
```
{
    "status": "success",
    "message": "Address of a post with id {post_id} has been updated successfully."
}
```


### Delete a post
URL: `/posts/{post_id}/`

Method: `DELETE`

Headers: Authorization = Bearer + JWT token

Response:
```
{
    "status": "success",
    "message": "Post with id {post_id} has been deleted successfully."
}
```