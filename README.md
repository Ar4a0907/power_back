## Power banks admin back-end

##### NOTE
For all listed below commands use your versions of python and pip

## Project setup

* Create virtual environment in project root directory:  
`sudo python3.9 -m venv venv`
* Activate virtual env(from project root dir):  
`. venv/bin/activate`
* Install dependencies(from root folder):  
`sudo pip3.9 install -r requirements.txt`
* To deactivate virtual env run:  
`deactivate`  
* Database creation(also can be used on db structure change). Inside root dir run(when venv activated):  
`python3.9`  
`from power_banks_admin import app`  
`from power_banks_admin.db import db`  
`db.init_app(app)`  
`with app.app_context():`  
`db.create_all()`  


##### NOTE
Install new dependencies only when you in virtual env. When all dependencies installed run(from project root dir):  
`pip3.9 freeze > requirements.txt`

## Run app
* Set flask app variable:  
`export FLASK_APP=power_banks_admin`
* Run app:  
`flask run`
