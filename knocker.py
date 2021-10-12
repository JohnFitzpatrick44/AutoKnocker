import time
import grovepi
import lcd_utilities

# Set pin addresses
SOUND_SENSOR_PIN = 0
RELAY_PIN = 6
LED_PIN = 5

# Knock constants
KNOCK_SOUND_THRESHOLD = 500
KNOCK_DURATION = 100
KNOCK_END_TIME_THRESHOLD = 2000
TRANSITION_TIME = 1000
TIME_STEP = 5

grovepi.pinMode(SOUND_SENSOR_PIN,"INPUT")
grovepi.pinMode(RELAY_PIN,"OUTPUT")
grovepi.pinMode(LED_PIN,"OUTPUT")

def get_time():
	"Returns current time in milliseconds."
	return round(time.time() * 1000)
	
def sleep(t):
	"Sleeps for t milliseconds."
	if t > 0:
		time.sleep(t / 1000)

def record_knocks():
	"Records a series of knocks, returning the time between them. Stops recording after KNOCK_END_TIME_THRESHOLD."
	output_times = []
	prev_time = get_time()
	lcd_utilities.set_text("Recording.")
	
	while True:
		# Read the sound level
		sound_value = grovepi.analogRead(SOUND_SENSOR_PIN)
		curr_time = get_time()
        
		# If above threshold, add delay to list
		if(sound_value > KNOCK_SOUND_THRESHOLD):
			grovepi.digitalWrite(LED_PIN, 1)
			
			output_times.append(curr_time - prev_time)
			prev_time = curr_time
			sleep(KNOCK_DURATION)
			
			grovepi.digitalWrite(LED_PIN, 0)
		
		# If knock has completed (we see a delay above the time threshold)
		if output_times:
			if curr_time - prev_time > KNOCK_END_TIME_THRESHOLD:
				return output_times
			
		sleep(TIME_STEP)
		
def knock():
	"Performs a knock."
	grovepi.digitalWrite(RELAY_PIN, 1)
	sleep(KNOCK_DURATION)
	grovepi.digitalWrite(RELAY_PIN, 0)
		
def play_knocks(input_times):
	"Plays back knocks based on delays given by input. The first knock occurs after the first delay."
	lcd_utilities.set_text("Replaying.")
	
	# Remove the first delay, as it represents the time between the start of the recording and the first knock
	input_times.pop(0)
	knock()
	
	for delay in input_times:
		sleep(delay - KNOCK_DURATION)
		grovepi.digitalWrite(LED_PIN, 1)
		knock()
		grovepi.digitalWrite(LED_PIN, 0)
	
lcd_utilities.set_text("Initializing")
lcd_utilities.set_color(0, 128, 64)
	
while True:
	try:
		knock_delays = record_knocks()
		play_knocks(knock_delays)
		sleep(TRANSITION_TIME)
	
	except KeyboardInterrupt:
		grovepi.digitalWrite(RELAY_PIN, 0)
		grovepi.digitalWrite(LED_PIN, 0)
		lcd_utilities.set_text("Stopping.")
		break
	except IOError:
		print ("Error")
		




