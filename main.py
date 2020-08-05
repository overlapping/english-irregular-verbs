from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import TextToSpeechV1
import time
import enum
import os
import vlc
import json


class Voice(enum.Enum):
    Allison = 'en-US_AllisonV3Voice'


class Accept(enum.Enum):
    WAV = 'wav'


class Tense(enum.Enum):
    Infinitive = 'infinitive'
    PastSimple = 'past simple'
    PastParticiple = 'past participle'


class Text:
    def __init__(self, text: str, voice: str, accept: str, text_to_speech: TextToSpeechV1):
        self.text = text
        self.voice = voice
        self.accept = accept
        self.audio_file = '%s.%s' % (self.text, self.accept)
        self.text_to_speech = text_to_speech

    def play(self):
        if not (self.__exists()):
            self.__generate_speech()
        vlc.MediaPlayer(self.audio_file).play()

    def __exists(self):
        return os.path.exists('./%s' % self.audio_file)

    def __generate_speech(self):
        with open(file=self.audio_file, mode='wb') as audio_file:
            audio_file.write(
                self.text_to_speech.synthesize(
                    text=self.text,
                    voice=self.voice,
                    accept='audio/%s' % self.accept
                ).get_result().content)

    def __str__(self):
        return 'text: ' % self.text


class Verb(Text):
    def __init__(self, text: str, voice: str, accept: str, text_to_speech: TextToSpeechV1, type: str, tenses: list, ):
        super(Verb, self).__init__(text, voice, accept, text_to_speech)
        self.type = type
        self.tenses = tenses

    def __str__(self):
        return 'type: %s tense: %s' % self.type, self.tenses


def main():
    apikey = os.getenv('TEXT_TO_SPEECH_IAM_APIKEY')
    service_url = os.getenv('TEXT_TO_SPEECH_URL')

    authenticator = IAMAuthenticator(apikey)
    text_to_speech = TextToSpeechV1(
        authenticator=authenticator
    )

    text_to_speech.set_service_url(service_url)

    verbs = []

    with open(file='data.json', mode='r') as json_file:
        data = json.load(json_file)
        for verb in data['verbs']:
            text, type, tenses = verb.values()
            verbs.append(Verb(text, Voice.Allison.value, Accept.WAV.value, text_to_speech, type, tenses))

    for verb in verbs:
        verb.play()

    # text = Text('been', Voice.Allison.value, Accept.WAV.value, text_to_speech)
    # text.play()

    #


if __name__ == "__main__":
    main()
