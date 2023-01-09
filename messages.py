from pychord import Chord
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

COMPOSE_MESSAGE = "Insert the list of notes divided by a space (_i.e. C E G_):"

def get_chord_analysis_message(chord: Chord):
	''' text = "Chord: *{}*\n".format(chord.chord)
	text += "Root: *{}*\n".format(chord.root)
	text += "Quality: *{}*\n".format(chord.quality)
	text += "On: *{}*\n".format(chord.on)
	text += "\nNotes: *{}*\n".format(chord.components()) '''

	text = tabulate([["Chord", f"*{chord.chord}*"], ["Root", f"*{chord.root}*"], ["Quality", f"*{chord.quality}*"], ["On", f"*{chord.on}*"], ["Notes", f"*{chord.components()}*"]], tablefmt="plain")
	return text