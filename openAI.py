# -*- coding: utf-8 -*-
import sys
OPENAI_SECRET_KEY = "--------------------APIKey---------------------"
OPENAI_ENGINE = 'gpt-3.5-turbo'


class api:    
    import openai

    message_post = [{"role":"system","content":"これからの会話は全て日本語で答えてください．"}]
    
    def __init__(self, key, engine = OPENAI_ENGINE):
        self.openai.api_key = key
        self.openai_engine = engine
    
    def send(self,prompt_content):
        print("please wait...(openAIAPI...)")
        self.message_post.append( {"role":"user","content":prompt_content})
        try:
            completions = self.openai.ChatCompletion.create(
                model = OPENAI_ENGINE,
                messages = self.message_post,
                temperature=0.5,
            )
            reply = completions.choices[0].message.content
            self.message_post.append({"role":"assistant","content":reply}) 

            if completions.usage.total_tokens > 3500:
                self.message_post.pop(1)
            return reply
        except :
            print(sys.exc_info())
            return ""


if __name__ == '__main__':    
    
    API = api(OPENAI_SECRET_KEY)
    prompt = input("Enter a prompt: ")

    while(prompt != "EXIT"):
        if prompt != "":
            print(API.send(prompt))
        prompt = input("Enter a prompt: ")
        
        
        
