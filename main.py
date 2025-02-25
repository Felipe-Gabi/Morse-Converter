from flask import Flask, render_template, request
import winsound  # For sound playback (Windows only)
import time      # For timing the beeps

app = Flask(__name__)

# Morse Code Dictionary
MORSE_DICT = {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.',
    'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..',
    'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.',
    's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
    'y': '-.--', 'z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----', ' ': '/', '.': '.-.-.-', ',': '--..--'
}

# Reverse Morse Dictionary for decoding
REVERSE_MORSE_DICT = {value: key for key, value in MORSE_DICT.items()}


# Function to play beeps for Morse code
def play_morse_sound(morse_code):
    for char in morse_code:
        if char == '.':
            winsound.Beep(750, 200)  # Short beep for dot (750 Hz, 200 ms)
        elif char == '-':
            winsound.Beep(750, 600)  # Long beep for dash (750 Hz, 600 ms)
        elif char == ' ':
            time.sleep(0.2)  # Short pause between letters
        elif char == '/':
            time.sleep(0.6)  # Long pause between words
        time.sleep(0.1)  # Short gap between symbols


@app.route("/", methods=["GET", "POST"])
def morse_code_converter():
    result = ""
    user_input = ""
    play_sound = False

    if request.method == "POST":
        # Get user input
        user_input = request.form.get("input_text", "").strip()

        # Check if the user clicked the "Play Morse Code" button
        if "play_sound" in request.form:
            result = request.form.get("morse_code", "")
            if result:
                play_morse_sound(result)  # Play the stored Morse code sound

        else:
            # Regular conversion logic
            if all(char in '.-/ ' for char in user_input):
                # Decode Morse Code to text
                try:
                    morse_words = user_input.split(' / ')
                    decoded_message = ''
                    for word in morse_words:
                        decoded_message += ''.join(
                            REVERSE_MORSE_DICT[char] for char in word.split() if char in REVERSE_MORSE_DICT
                        ) + ' '
                    result = decoded_message.strip()
                except KeyError:
                    result = "Error: Invalid Morse code input."
            else:
                # Encode text to Morse Code
                try:
                    user_input = user_input.lower()
                    result = ' '.join(MORSE_DICT[char] for char in user_input if char in MORSE_DICT)
                except KeyError:
                    result = "Error: Invalid text input."

    return render_template("index.html", result=result, user_input=user_input)


if __name__ == "__main__":
    app.run(debug=True)
