# watermark-site
This is part of my graduation project! a very simple context manager system!
It's can register a new user and login/logout,etc.It's also can upload your
image and download your image! a very simple gallery system!I design it for
my digit watermark system demo!if you like follow the below step, you can get
it and hope you can enjoy it!

Get it Now
----------
```shell
mkdir ~/site
cd site
virtualenv env
source ./env/bin/activate
git clone https://github.com/land-pack/watermark-site.git
cd watermark-site
pip install -r requirements.txt
```

Set environment variable
------------------------
If you use mysql as your endpoint , you should create a database first!
```shell
export SECRET_KEY='some hard to guess string'
export MAIL_USERNAME='your-email-username'
export MAIL_PASSWORD='your-email-password'
export DATABASE_URL='mysql://root:123456@127.0.0.1:3306/watermark_site'
export WATERMARK_CONFIG='production'
```
Create a database by mysql client
---------------------------------
```shell
create database watermark_site
```
Configure your app
------------------
In this app,client can  will upload some image to the server! so you need to get a path for the app!
and i have default setting! but on Linux ,you should get a permission to the app! simple run a shell
```shell
sudo mkdir /var/lib/watermark-site
sudo chmod a+w /var/lib/watermark-site/
```
Change the configure to production mode if you want to run it on production!
----------------------------------------------------------------------------
you need to install `mysql-python`
```shell
pip install mysql-python
```
also you need to tell the server run on the `production` config mode!
```shell
export WATERMARK_CONFIG='production'
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

Ref
--
http://stackoverflow.com/questions/22312014/flask-redirecturl-for-error-with-gunricorn-nginx
