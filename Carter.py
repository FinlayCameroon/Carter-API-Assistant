# Carter Api Client by Finlay Cameron
# https://github.com/FinlayCameroon

import requests
from pygame import mixer
import os
import time


class CarterClient:
    def __init__(self, API_KEY):
        self.API_KEY: str = API_KEY
        self.PATH: str = os.path.abspath(os.getcwd())

    def ApiRequest(self, Query):
        request = requests.post("https://api.carterapi.com/v0/chat", json={
            'api_key': f'{self.API_KEY}',
            'query': f'{Query}',
            'uuid': 'user-id-123'
        })
        try:
            agentResponse = request.json()
        except:
            agentResponse :str = "Api Error" # I think its an api error anyways aha
        return agentResponse

    def OutputText(self, ApiResponse):
        if (ApiResponse) != ("Api Error"):
            outputText = ApiResponse['output']['text']
        else:
            outputText = "Api Error"
        return outputText

    def CustomTrigger(self, ApiResponse):
        if (ApiResponse) != ("Api Error"):
            try:
                customTriggerRes = ApiResponse['triggers'][0]
            except TypeError:
                customTriggerRes = ApiResponse['triggers']
            try:
                trigger: str = customTriggerRes["type"]
            except TypeError:
                trigger :str = "None Activated"
            return trigger
        else:
            return "Api Error"


    def EntityRecognition(self, ApiResponse):
        if (ApiResponse) != ("Api Error"):
            try:
                entities = ApiResponse['triggers'][0]['entities']
                
            except TypeError:
                entities = "None"
            if (entities) != ("None"):
                try:
                    entityWord: str = entities['word']
                    entityLabel: str = entities['label']
                except TypeError:
                    entityWord: str = "No Entities Found"
                    entityLabel: str = "No Entities Found"
            else:
                entityWord: str = "No Entities Found"
                entityLabel: str = "No Entities Found"
            return entityWord, entityLabel
        else:
            return "Api Error"    
        

    def Sentiment(self, ApiResponse):
        if (ApiResponse) != ("Api Error"):
            sentiment = ApiResponse['sentiment']
            sentimentInput = sentiment['input']
            sentimentInputLabel: str = sentimentInput['label']
            sentimentOutput = sentiment['output']
            sentimentOutputLabel: str = sentimentOutput['label']
            sentimentSession = sentiment['session']
            sentimentSessionLabel: str = sentimentSession['label']
            return sentimentInputLabel, sentimentOutputLabel, sentimentSessionLabel
        else:
            return "Api Error"

    def Question(self, ApiResponse):
        if (ApiResponse) != ("Api Error"):
            question: bool = ApiResponse['question']
            return question
        else:
            return "Api Error"

    def OutputText(self, ApiResponse):
        if (ApiResponse) != ("Api Error"):
            output = ApiResponse['output']
            outputText: str = output['text']
            return outputText
        else:
            return "Api Error"

    def SpeechSynthesis(self, TextToBeSpoken):
        voice = requests.get(
            f"https://api.carterapi.com/v0/speak/{self.API_KEY}/{TextToBeSpoken}", stream=True)
        with open(f"{self.PATH}\\temp.mp3", "wb") as f:
            for chunk in voice.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        mixer.init()
        mixer.music.load(f"{self.PATH}\\temp.mp3")
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(1)
        mixer.quit()
        os.remove(f"{self.PATH}\\temp.mp3")



