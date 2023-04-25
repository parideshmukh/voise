#Import necessary modules
import sounddevice as sd
import queue
import soundfile as sf
from flask import Flask, render_template,request, Response

import sqlite3
import pymysql
import numpy as np
import wave
import mysql.connector
from flask_cors import CORS
import numpy as np
import librosa
from flask import redirect, url_for
from flask import Flask, render_template,request, Response

 #create a connection to the database
conn = mysql.connector.connect(user='root', password='root',
                               host='localhost', database='employee')



 # prepare a cursor object
cursor = conn.cursor()


cursor.execute("CREATE TABLE IF NOT EXISTS candidate0 (id INT AUTO_INCREMENT PRIMARY KEY, audio_data1 LONGBLOB, audio_data2 LONGBLOB)")


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

 #Fit data into queue
def callback(indata, frames, time, status):
   q.put(indata.copy())
 #Recording function

@app.route('/startskill', methods=['GET', 'POST'])
def startskill():
   #Declare global variables   
   global recording
   #Set to True to record
   recording= True  
   global file_exists
   #Create a file to save the audio
   #messagebox.showinfo(message="Recording Audio. Speak into the mic")
   with sf.SoundFile("output1.wav", mode='w', samplerate=44100,
                       channels=2) as file:
       #Create an input stream to record audio without a preset time
       with sd.InputStream(samplerate=44100, channels=2, callback=callback):
           while recording == True:
               #Set the variable to True to allow playing the audio later
               file_exists =True
               #write into file
               file.write(q.get())
   return "recording start"


 #Create a queue to contain the audio data
q = queue.Queue()
 # Declare variables and initialise them
@app.route('/stopskill', methods=['GET', 'POST'])
def stopskill():
    global recording
    recording = False
    return"recording stop"



 #for replay audio

@app.route('/playskill', methods=['GET', 'POST'])
def playskill():
    if file_exists:
           #Read the recording if it exists and play it
           data, fs = sf.read("output1.wav", dtype='float32')
           sd.play(data,fs)
           sd.wait()
    return "audio are started"

def callback(indata, frames, time, status):
 q.put(indata.copy())
 #Recording function

@app.route('/startexprience', methods=['GET', 'POST'])
def startexprience():
   #Declare global variables   
   global recording
   #Set to True to record
   recording= True  
   global file_exists
   #Create a file to save the audio
   #messagebox.showinfo(message="Recording Audio. Speak into the mic")
   with sf.SoundFile("output2.wav", mode='w', samplerate=44100,
                       channels=2) as file:
       #Create an input stream to record audio without a preset time
       with sd.InputStream(samplerate=44100, channels=2, callback=callback):
           while recording == True:
               #Set the variable to True to allow playing the audio later
               file_exists =True
               #write into file
               file.write(q.get())
   return "recording start"


 #Create a queue to contain the audio data
q = queue.Queue()
 #Declare variables and initialise them
@app.route('/stopexprience', methods=['GET', 'POST'])
def stopexprience():
    global recording
    recording = False
    return"recording stop"



 #for replay audio

@app.route('/playexprience', methods=['GET', 'POST'])
def playexprience():
    if file_exists:
          
           data, fs = sf.read("output2.wav", dtype='float32')
           sd.play(data,fs)
           sd.wait()
    return "audio are started"



@app.route('/submit', methods=['POST'])
def submit():
  
    with open("output1.wav", "rb") as audio_file:
        audio_data1 = audio_file.read()
    with open("output2.wav", "rb") as audio_file:
        audio_data2 = audio_file.read()
      
    contact_number = request.form.get('contact_number')
    
    sql = "INSERT INTO candidate0 (audio_data1, audio_data2) VALUES (%s, %s)"
    
    val = ( audio_data1, audio_data2,)
    cursor.execute(sql, val)
    conn.commit()
   
    print(cursor.rowcount, "record inserted.")
    return 'voise is recorded'


 

 
if __name__ == '__main__':
    app.run(debug=True)




