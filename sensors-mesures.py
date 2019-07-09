#!/usr/bin/python
 
import spidev
import os
import time
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
import google.cloud

cred = credentials.Certificate("path/to/file.json")
delay = 0.2

Config = {

  "apiKey": " ",
  "authDomain": " ",
  "databaseURL": " ",
  "projectId": " ",
  "storageBucket": " ",
  "messagingSenderId": " ",
  "appId": " ",
  "cred"}

firebas = pyrebase.initialize_app(Config)
auth = firebas.auth()
firebase = firebase_admin.initialize_app(config)
db = firestore.client()
user = auth.get_user(uid)
 
spi = spidev.SpiDev()
spi.open(0,0)
 
def readChannel(channel):
  email = input ("entrez votre adresse email: \n")
  password = input ("entrez votre password: \n")

  val = spi.xfer2([1,(8+channel)<<4,0])
  data = ((val[1]&3) << 8) + val[2]
  return data
 
if __name__ == "__main__":
  try:
    while True:
      try:
        auth.sign_in_with_email_and_password(email, password)
        return'login successfully completed'
      except:
        return 'Check your credentials'

      val = readChannel(0)
      if (val != 0):
        
        user_id_ref= db.collection(u'users').document(u'user.uid')
        moisture_ref = user_id_ref.collection(u'values_mesured').document(u'moisture')
        moisture_ref.set(val)
        print(val)
      time.sleep(delay)
      
  except KeyboardInterrupt:
    print ("Cancel.")