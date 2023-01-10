from pychord import Chord, find_chords_from_notes
from tabulate import tabulate

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

def get_chord_analysis_message(chord: Chord):
	text = "*Chord:* `{}`\n\n".format(chord.chord)
	text += "*Root:* `{}`\n".format(chord.root)
	text += "*Quality:* `{}`\n".format(chord.quality)
	text += "*On:* `{}`\n\n".format(chord.on)
	text += "*Notes:* `{}`\n".format(chord.components())

	# text = tabulate([["Chord", f"*{chord.chord}*"], ["Root", f"*{chord.root}*"], ["Quality", f"*{chord.quality}*"], ["On", f"*{chord.on}*"], ["Notes", f"*{chord.components()}*"]], tablefmt="plain")
	return text

def get_compose_analysis_message(notes):
	try:
		chords = find_chords_from_notes(notes)
	except ValueError as e:
		return f"*{str(e)}*"
	
	text = "*Possible chords:*\n"
	for c in chords:
		text += f"`{c.chord}`\n"
	return text