import os

class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'you-will-never-guess'
    TWILIO_SID = os.environ['TWILIO_SID']
    TWILIO_TOKEN = os.environ['TWILIO_TOKEN']
    TWILIO_MESSAGING_SERVICE = os.environ['TWILIO_MESSAGING_SERVICE']