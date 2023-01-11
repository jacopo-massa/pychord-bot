from pychord import Chord, find_chords_from_notes

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
