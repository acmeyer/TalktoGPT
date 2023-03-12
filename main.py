import os
import openai
import datetime
import argparse
from dataclasses import asdict
from models import Message
import speech_recognition as sr
from google.cloud import texttospeech
import logging
logging.basicConfig(level=logging.INFO)

CHAT_MODEL = "gpt-3.5-turbo"
AUDIO_MODEL = "whisper-1"
MODEL_TEMPERATURE = 1.0

def ask_gpt3_chat(prompt: str, messages: list[Message]):
    """Returns ChatGPT-3's response to the given prompt."""
    system_message = [{"role": "system", "content": prompt}]
    if len(messages) > 0:
        message_dicts = [asdict(message) for message in messages]
        conversation_messages = system_message + message_dicts
    else:
        conversation_messages = system_message
    logging.info('Getting response from GPT-3...')
    response = openai.ChatCompletion.create(
        model=CHAT_MODEL,
        messages=conversation_messages,
        temperature=MODEL_TEMPERATURE,
    )
    return response.choices[0]['message']['content'].strip()


def setup_prompt() -> str:
    """Creates a prompt for gpt-3 for generating a response."""
    with open('prompt.md') as f:
        prompt = f.read()

    return prompt


def get_filename_for_file_path(file_path: str) -> str:
    return file_path.split('/')[-1].split('.')[0]


def get_transcription(file_path: str):
    audio_file= open(file_path, "rb")
    return openai.Audio.transcribe(
        model=AUDIO_MODEL, 
        file=audio_file
    )

def record():
    # load the speech recognizer with CLI settings
    r = sr.Recognizer()

    # record audio stream from multiple sources
    m = sr.Microphone()

    with m as source:
        logging.info(f'Listening...')
        audio = r.listen(source)

    # write audio to a WAV file
    timestamp = datetime.datetime.now().timestamp()
    with open(f"./recordings/{timestamp}.wav", "wb") as f:
        f.write(audio.get_wav_data())
    transcript = get_transcription(f"./recordings/{timestamp}.wav")
    with open(f"./transcripts/{timestamp}.txt", "w") as f:
        f.write(transcript['text'])
    return transcript['text']

def text_to_speech(text: str):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    logging.info('Getting audio for the response...')
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    timestamp = datetime.datetime.now().timestamp()
    with open(f"outputs/{timestamp}.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
    return f"outputs/{timestamp}.mp3"

def clean_up():
    logging.info('Exiting...')
    # Delete all the recordings and transcripts
    for file in os.listdir('./recordings'):
        os.remove(f"./recordings/{file}")
    for file in os.listdir('./transcripts'):
        os.remove(f"./transcripts/{file}")
    for file in os.listdir('./outputs'):
        os.remove(f"./outputs/{file}")
    # Save the conversation
    timestamp = datetime.datetime.now().timestamp()
    with open(f'logs/conversation_{timestamp}.txt', 'w') as f:
        for message in conversation_messages:
            f.write(f"{message.role}: {message.content}\n")

if __name__ == "__main__":
    # Setup the bot
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--stop_word", help="Specify the stop word to use.", type=str, default="bye")
    parser.add_argument("-v", "--voice", help="Specify the voice to use.", type=str, default="Google", choices=["Google", "macOS"])
    args = parser.parse_args()
    stop_word = args.stop_word
    voice = args.voice

    prompt = setup_prompt()
    conversation_messages = []
    while True:
        try:
            user_input = record()
            logging.info(f'User: {user_input}')
            conversation_messages.append(Message(role="user", content=user_input))
            answer = ask_gpt3_chat(prompt, conversation_messages)
            logging.info(f'Bot: {answer}')
            logging.info('Playing audio...')
            if voice == "macOS":
                os.system(f'say "{answer}"')
            else:
                audio_file = text_to_speech(answer)
                # Play the audio file
                os.system(f"afplay {audio_file}")
            conversation_messages.append(Message(role="assistant", content=answer))
            if stop_word and (stop_word.lower() in user_input.lower()):
                clean_up()
                break
        except KeyboardInterrupt:
            clean_up()
            break

    
