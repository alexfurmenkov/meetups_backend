### Applying Migrations
Migrations are essential to transit the DB into the working state. 

**First, ensure that you have a postgres DB called "meetups_db" created and running.**

Then, execute default Django commands:

`python src/manage.py makemigrations meetups_backend`

`python src/manage.py migrate`

Finally, the DB must be populated with data about the post types. 
Unfortunately, there is no way to automate Django data migrations (only schema migrations can be automated), 
so the separate command has to be executed:

`python src/manage.py loaddata --app meetups_backend post_type.json`
