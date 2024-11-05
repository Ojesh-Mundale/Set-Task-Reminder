from flask import Flask, render_template, request, redirect, url_for
import time
import threading
from plyer import notification
from playsound import playsound

app = Flask(__name__)

def send_notification(message):
    notification.notify(
        title="Reminder",
        message=message,
        app_name="Reminder App",
        timeout=10  # Notification stays for 10 seconds
    )

def play_sound(sound_file):
    playsound(sound_file)

def reminder(message, delay, sound_file):
    time.sleep(delay)
    send_notification(message)
    play_sound(sound_file)

@app.route('/', methods=['GET', 'POST'])
def set_reminder():
    if request.method == 'POST':
        message = request.form['message']
        minutes = int(request.form['minutes'])
        seconds = int(request.form['seconds'])
        
        # Convert the total delay into seconds
        total_delay = (minutes * 60) + seconds
        
        # Specify the path to your sound file
        sound_file = 'sound.wav'  # Change this to your sound file's path
        
        # Start the reminder in a separate thread
        threading.Thread(target=reminder, args=(message, total_delay, sound_file)).start()
        
        return redirect(url_for('set_reminder'))  # Redirect to avoid form resubmission
    
    return render_template('reminder.html')

if __name__ == "__main__":
    app.run(debug=True)