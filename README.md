# watermark-site
This is part of my graduation project

Prepare your env
----------------
##### Set some variable for env
```shell
export SECRET_KEY='some hard to guess string'
export MAIL_USERNAME='your-email-username'
export MAIL_PASSWORD='your-email-password'
```

#### Init database 
```shell
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```
