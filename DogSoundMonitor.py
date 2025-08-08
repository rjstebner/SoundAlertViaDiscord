import sounddevice as sd
import numpy as np
import simpleaudio as sa
import requests
from collections import deque
import time

# Settings
LOUD_THRESHOLD = 16
REALLY_LOUD_THRESHOLD = 50.0
COOLDOWN = 5
AUDIO_FILE = "No_Bonk_No.wav"
DISCORD_WEBHOOK_URL = "Add your own url here"
TRIGGER_LIMIT = 3        # max allowed triggers
TRIGGER_WINDOW = 20      # seconds window

last_trigger_time = 0



def play_audio():
	try:
		wave_obj = sa.WaveObject.from_wave_file(AUDIO_FILE)
		play_obj = wave_obj.play()
	except Exception as e:
		print(f"[ERROR] playing audio {e}")

def send_discord_message(content):
	try:
		requests.post(DISCORD_WEBHOOK_URL, json={"content": content})
		print(f"{content} sent to discord")
	except Exception as e:
		print(f"[ERROR] sending message to discord {e}")


trigger_times = deque()

def check_trigger():
    current_time = time.time()
    
    # Remove triggers older than TRIGGER_WINDOW seconds
    while trigger_times and trigger_times[0] < current_time - TRIGGER_WINDOW:
        trigger_times.popleft()
    
    # Add current trigger time
    trigger_times.append(current_time)
    
    # If too many triggers in window, alert!
    if len(trigger_times) > TRIGGER_LIMIT:
        print(f"Alert: Threshold triggered {len(trigger_times)} times in {TRIGGER_WINDOW} seconds!")
        send_discord_message("Laura the audio aint working she wont stop!!")

def doing_the_stuff(indata,frames,time_info, status):
	global last_trigger_time

	if status:
		print(status)
	
	now = time.time()
	readable = time.strftime("%H:%M:%S", time.localtime(now))


	volume_norm = np.linalg.norm(indata) * 10
	if volume_norm > 10:
		print(f"Volume: {volume_norm:.4f} at {readable}")


	current_time = time.time()
	if current_time - last_trigger_time < COOLDOWN:
		return
	
	if volume_norm > REALLY_LOUD_THRESHOLD:
		check_trigger()
		send_discord_message("Laura it's loud af right now")
		play_audio()
		last_trigger_time = current_time
	elif volume_norm > LOUD_THRESHOLD:
		check_trigger()
		play_audio()
		last_trigger_time = current_time

mic_id = 41
print("🎤 Listening... Press Ctrl+C to stop.")
try:
    with sd.InputStream(device=mic_id, callback=doing_the_stuff):
        while True:
            time.sleep(0.1)
except KeyboardInterrupt:
    print("\n🛑 Stopped by user. Goodbye!")
