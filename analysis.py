import os
import requests

from pychord import Chord, find_chords_from_notes

IMGBUN_API_KEY = os.getenv('IMGBUN_API_KEY')

CHORD_URL = "https://www.scales-chords.com/api/scapi.1.3.php"
THUMBNAIL_URL = f"https://api.imgbun.com/jpg"


def get_chord_analysis_message(chord: Chord):
	text = "*Chord:* `{}`\n\n".format(chord.chord)
	text += "*Root:* `{}`\t\t\t".format(chord.root)
	text += "*Quality:* `{}`\t\t\t".format(chord.quality)
	text += "*On:* `{}`\n\n".format(chord.on)
	text += "*Notes:* `{}`\n".format(', '.join(chord.components()))

	return text


def get_compose_analysis_message(notes):
	chords = find_chords_from_notes(notes)
	
	if chords:
		text = "*Possible chords:*\n"
		text += "`{}`".format(', '.join([c.chord for c in chords]))
	else:
		text = "*No possible chords*"
	return text


def get_chord_image_url(chord: Chord):
	url = requests.post(CHORD_URL, data={"chord": chord.chord, "instrument": "piano"}).text.split("src=")[1][1:-2]
	return url

def get_thumb_image_url(text):
	url = requests.get(THUMBNAIL_URL, params={"key": IMGBUN_API_KEY, "text": text, "size": 5}).json()["direct_link"]
	return url