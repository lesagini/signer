import serial
import os
import signals
import sys
import joblib
import pyttsx


engine = pyttsx.init()
sound = engine.getProperty('voices')
engine.setProperty('voice', sound[0].id)


def print_sentence_with_pointer(sentence_argument, position):
	print(sentence_argument)
	new_cursor_position = " " * position + "^"
	print(new_cursor_position)

# ALTERNATIVE: the quick brown fox jumps over the lazy dog


test_sentence = "pack my box with five dozen liquor jugs"

# Mode parameters
TRY_TO_PREDICT = False
SAVE_NEW_SAMPLES = False
FULL_CYCLE = False
ENABLE_WRITE = False
TARGET_ALL_MODE = False
DELETE_ALL_ENABLED = False

SERIAL_PORT = "COM6"
BAUD_RATE = 38400
TIMEOUT = 100

target_sign = "a"
current_batch = "0"
target_directory = "data"
final_dict = {}
current_test_index = 0
arguments = {}
root_folder_for_dict = "data"


def get_final_dictionary():
	for path_of_dict, subdirectories, files in os.walk(root_folder_for_dict):
		for name in files:
			category = name.split("_")[0]
			string_id = ""
			for parts in category:
				string_id += str(ord(parts))
			final_dict[string_id] = category
	return final_dict


for i in sys.argv[1:]:
	if "=" in i:
		sub_args = i.split("=")
		arguments[sub_args[0]] = sub_args[1]
	else:
		arguments[i] = None


if len(sys.argv) > 1:
	if "target" in arguments:
		target_sign = arguments["target"].split(":")[0]
		current_batch = arguments["target"].split(":")[1]
		print(f"TARGET SIGN: '{target_sign}' USING BATCH: {current_batch}")
		SAVE_NEW_SAMPLES = True
	if "predict" in arguments:
		TRY_TO_PREDICT = True
	if "write" in arguments:
		TRY_TO_PREDICT = True
		ENABLE_WRITE = True
	if "test" in arguments:
		current_batch = arguments["test"]
		TARGET_ALL_MODE = True
		SAVE_NEW_SAMPLES = True
	if "port" in arguments:
		SERIAL_PORT = arguments["port"]

clf = None
classes = None
sentence = ""

if TRY_TO_PREDICT:
	print("Loading model...")
	clf = joblib.load('model.pkl')
	classes = joblib.load('classes.pkl')

print(f"OPENING SERIAL_PORT '{SERIAL_PORT}' WITH BAUDRATE {BAUD_RATE}...")

print("IMPORTANT!")
print("To end the program hold Ctrl+C and send some data over serial")

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)

output = []

in_loop = True
is_recording = False

current_sample = 0

output_file = open("output.txt", "w")
output_file.write("")
output_file.close()

if TARGET_ALL_MODE:
	print_sentence_with_pointer(test_sentence, 0)

try:
	while in_loop:
		line = ser.readline().decode("utf-8").replace('\r\n', '')
		print(line)
		if line == "STARTING BATCH":
			is_recording = True
			output = []
			print("RECORDING..."),
		elif line == "CLOSING BATCH":
			is_recording = False
			if len(output) > 1:  # If less than 1, it means error
				print("DONE, SAVING..."),

				if TARGET_ALL_MODE:
					if current_test_index < len(test_sentence):
						target_sign = test_sentence[current_test_index]
					else:
						print("Target All Ended!")
						quit()

				filename = f"{target_sign}_sample_{current_batch}_{current_sample}.txt"
				path = target_directory + os.sep + filename
				
				if not SAVE_NEW_SAMPLES:
					path = "tmp.txt"
					filename = "tmp.txt"

				f = open(path, "w")
				f.write('\n'.join(output))
				f.close()
				print(f"SAVED IN {filename}")

				current_sample += 1

				if TRY_TO_PREDICT:
					print("PREDICTING...")
					sample_test = signals.Sample.load_from_file(path)
					linearized_sample = sample_test.get_linearized(reshape=True)
					number = clf.predict(linearized_sample)
					new_number = str(number).replace("[", "").replace("]", "")
					new_number = [f'{new_number}']
					fd = get_final_dictionary()
					for word in new_number:
						char = fd.get(word)
					
					if ENABLE_WRITE:
						if char == 'D':  # Delete the last character
							sentence = sentence[:-1]
						elif char == 'A':  # Delete all characters
							if DELETE_ALL_ENABLED:
								sentence = ""
							else:
								print("DELETE_ALL_ENABLED = FALSE")
						else:  # Add the char to the sentence
							if len(char) > 1:
								sentence += char + " "
							else:
								sentence += char
						# Prints the last char and the sentence
						print(f"[{char}] -> {sentence}")
						# Save  to file
						output_file = open("output.txt", "w")
						output_file.write(sentence)
						output_file.close()
					else:
						print(char)
						engine.say(char)
						engine.runAndWait()
						# sentence = "hello"
						if len(char) > 1:
							sentence += " "+char + " "
						else:
							sentence += char

					output_file = open("output.txt", "w")
					if len(sentence) > 90:
						sentence = sentence.replace(sentence[0:5], "")
					output_file.write(sentence)
					output_file.close()									
			else:  # In case of a corrupted sequence
				print("ERROR...")
				current_test_index -= 1

			if TARGET_ALL_MODE:
				current_test_index += 1
				print_sentence_with_pointer(test_sentence, current_test_index)
		else:
			output.append(line)
except KeyboardInterrupt:
	print('CLOSED LOOP!')
	ser.close()


