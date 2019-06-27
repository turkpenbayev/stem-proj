# Diploma 

**An complete Flask application template, with useful plugins.**

Use this Flask app to initiate your project with less work. In this application  template you will find the following plugins already configured:

* **Flask** - Flask-Login provides user session management for Flask.
* **Flask-SocketIO** - Ready-to-use Twitter-bootstrap for use in Flask.

## Requirements

Python 3.5+, python-pip, virtualenv

## Instalation

To install virtualenv globally with pip (if you have pip 1.3 or greater installed globally):

    $ python3 -m pip install virtualenv

Create a virtualenv, and activate this: 

    $ python3 -m venv env 
    $ source env/bin/activate

After, install all necessary to run:

    $ pip install -r req.txt

Than, run the application and socket:

	$ python main.py
    $ python mqtt.py 

To see your application, access this url in your browser: 

	http://0.0.0.0:5000

