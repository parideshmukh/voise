#Import necessary modules
import sounddevice as sd
import queue
import soundfile as sf
from flask import Flask, render_template,request, Response
import numpy as np
import librosa
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import sqlite3
import pymysql
import numpy as np
import wave
import mysql.connector
from flask import redirect, url_for
import numpy as np
import librosa

 #create a connection to the database
conn = mysql.connector.connect(user='root', password='root',
                               host='localhost', database='employee')



 # prepare a cursor object
cursor = conn.cursor()



cursor.execute("CREATE TABLE IF NOT EXISTS authentication1 (aid INT AUTO_INCREMENT PRIMARY KEY, audio LONGBLOB)")


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index1.html')

 #Fit data into queue
def callback(indata, frames, time, status):
   q.put(indata.copy())
 #Recording function

@app.route('/start', methods=['GET', 'POST'])
def start():
   #Declare global variables   
   global recording
   #Set to True to record
   recording= True  
   global file_exists
   #Create a file to save the audio
   #messagebox.showinfo(message="Recording Audio. Speak into the mic")
   with sf.SoundFile("trial.wav", mode='w', samplerate=44100,
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
@app.route('/stop', methods=['GET', 'POST'])
def stop():
    global recording
    recording = False
    return"recording stop"

@app.route('/submit', methods=['POST'])
def submit():
 
    with open("trial.wav", "rb") as audio_file:
        audio = audio_file.read()
   
    
    sql = "INSERT INTO authentication1 (audio) VALUES (%s)"
    
    val = (audio,)
    cursor.execute(sql, val)
    conn.commit()
    
    return 'voise is recorded'




# Define a function to extract features from the audio signal
def extract_features(audio, sr):
    # Extract mel-spectrogram features
    mel_spec = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=128, fmax=8000)
    log_mel_spec = librosa.power_to_db(mel_spec, ref=np.max)

    # Resize the feature to match the input shape of the CNN model
    resized_spec = np.resize(log_mel_spec, (128, 660, 1))
    return resized_spec

# Define a function to build the CNN model
def build_model(input_shape):
    model = Sequential()
    model.add(Conv2D(32, (2, 2), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (2, 2), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, (2, 2), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    optimizer = Adam(learning_rate=0.0001)
    model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    return model



   


@app.route('/compare', methods=['GET', 'POST'])
def compare():
# Load the pre-recorded audio files for the speaker
 audio_files = ['output1.wav', 'output2.wav']
 audio_signals = [librosa.load(f, sr=16000)[0] for f in audio_files]

 # Extract features from the audio signals
 features = np.array([extract_features(audio, 16000) for audio in audio_signals])

 # Create labels for the features
 labels = np.array([1, 0]) 

 # Define the input shape of the CNN model
 input_shape = (128, 660, 1)

 # Build the CNN model
 model = build_model(input_shape)

 # Train the CNN model
 model.fit(features, labels, epochs=30, batch_size=55)

 # Load a new audio signal to be identified
 new_audio = librosa.load('trial.wav', sr=16000)[0]

 # Extract features from the new audio signal
 new_features = np.array([extract_features(new_audio, 16000)])

 # Make a prediction using the CNN model
 prediction = model.predict(new_features)
 print("Prediction:", prediction[0][0])
 if prediction > 0.9:
        message = "Speaker is a match."
 else:
        message = "Sorry, voice does not match."

 return message






 
if __name__ == '__main__':
    app.run(debug=True)



 





