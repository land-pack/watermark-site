# watermark-site
This is part of my graduation project! a very simple context manager system!
It's can register a new user and login/logout,etc.It's also can upload your
image and download your image! a very simple gallery system!I design it for
my digit watermark system demo!if you like follow the below step, you can get
it and hope you can enjoy it!

Get it Now
----------
```shell
virtualenv watermark-site-env
cd watermakr-site-env
mkdir src
cd src
git clone ...
source ./bin/activate
cd watermark-site
pip install -r requirements.txt
```

Set environment variable
------------------------
```shell
export SECRET_KEY='some hard to guess string'
export MAIL_USERNAME='your-email-username'
export MAIL_PASSWORD='your-email-password'
```

Init database 
-------------
```shell
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```
Run it
------
python manage.py runserver
