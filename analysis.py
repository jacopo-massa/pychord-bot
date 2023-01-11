from pychord import Chord, find_chords_from_notes

def get_chord_analysis_message(chord: Chord):
	text = "*Chord:* `{}`\n\n".format(chord.chord)
	text += "*Root:* `{}`\n".format(chord.root)
	text += "*Quality:* `{}`\n".format(chord.quality)
	text += "*On:* `{}`\n\n".format(chord.on)
	text += "*Notes:* `{}`\n".format(chord.components())

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