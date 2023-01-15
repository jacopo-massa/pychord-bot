import os
import requests

from pychord import Chord, find_chords_from_notes


CHORD_URL = "https://www.scales-chords.com/api/scapi.1.3.php"

WELCOME_MESSAGE = "This bot can help you analysing and composing chords! 🎹 🎸\n\nType /help or '/' to see the full list of available operations!"

HELP_MESSAGE = "*List of all available commands*:\n \
	\t /start -  Start the bot\n \
	\t /help  -  Show this message\n \
	\t /chord  -  Analyse a chord\n \
	\t /compose  -  Find chord(s) from notes\n\n"
#Type /help <command> to get more info about a specific command."

CHORD_MESSAGE = "Insert the chord you want to analyse, in the following format: \n \
*[<chord>]* (_i.e. [Am7]_)"

COMPOSE_MESSAGE = "Insert the list of notes in the following format: \n \
*{<note1> <note2> ... <noteN>}* (_i.e. {C E G}_):"

# CHORD ANALYSIS MESSAGE
def get_chord_analysis_message(chord: Chord):
	text = "*Chord:* `{}`\n\n".format(chord.chord)
	text += "*Root:* `{}`\t\t\t".format(chord.root)
	text += "*Quality:* `{}`\t\t\t".format(chord.quality)
	text += "*On:* `{}`\n\n".format(chord.on)
	text += "*Notes:* `{}`\n".format(', '.join(chord.components()))

	return text

# COMPOSE ANALYSIS MESSAGE
def get_compose_analysis_message(notes):
	chords = find_chords_from_notes(notes)
	
	if chords:
		text = "*Possible chords:*\n"
		text += "`{}`".format(', '.join([c.chord for c in chords]))
	else:
		text = "*No possible chords*"
	return text

# CHORD IMAGE URL using scales-chords.com API
def get_chord_image_url(chord: Chord):
	url = requests.post(CHORD_URL, data={"chord": chord.chord, "instrument": "piano"}).text.split("src=")[1][1:-2]
	return url
