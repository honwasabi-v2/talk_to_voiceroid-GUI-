# -*- coding: utf-8 -*-

ENDPOINT = 'https://api.a3rt.recruit.co.jp/talk/v1/smalltalk'
SECRET_KEY = "--------------------APIKey---------------------"

import requests

class api:
    def __init__(self, key, endpoint = ENDPOINT):
        self.apikey = key
        self.endpoint = endpoint

    def send(self, message):
        data = {
            'apikey': self.apikey,
            'query': message,
        }
        print("please wait...(A3RTAPI....)")
        json = requests.post(self.endpoint, data).json()
        #通常は{'status': 0, 'message': 'ok', 'results': [{'perplexity': 数値, 'reply': 文字列}]}
        #errだと{'status': 1400, 'message': 'bad request'}etc
        if json['status'] == 0:
            reply = json['results'][0]['reply']
        else:
            print(json)
            print('json_err:status ' + str(json['status']))
            return "json error"
        return reply
    

if __name__ == '__main__': 
    API = api(SECRET_KEY)
    print(API.send(input("input:")))
    


