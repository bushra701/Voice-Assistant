import openai
import pyttsx3
import speech_recognition as sr



#use your api key here
openai.api_key = ""

engine = pyttsx3.init()

def audiototext(filename):
    recognizer = sr.Recognizer()

    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)

    try:
 
        return recognizer.recognize_google(audio)
    except Exception as e:
        print(f"Error: {e}")
        return None

def responses(prompt):
    response = openai.Completion.create(
    model="gpt-3.5-turbo", 
    prompt = prompt,
    max_tokens = 4000,
    n = 1,
    stop = None,
    temperature = 0.5
)

    return response["choices"][0]["text"]

def speaktext(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        print("Say 'Hello' to record your question")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "hello":
                    filename = "input.wav"
                    print("Say your question")
                    with sr.Microphone() as source:  #
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                    text = audiototext(filename)
                    if text:
                        
                        print(f"You said: {text}")
                        response = responses(text)
                        print(f"GPT-3 says: {response}")
                        speaktext(response)

            except Exception as e:
                print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
