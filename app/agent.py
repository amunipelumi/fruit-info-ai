from groq import Groq
from os.path import abspath, dirname, join
import environ
import json


env = environ.Env()
environ.Env.read_env(join(dirname(dirname(abspath(__file__)))), '.env')
api_key = env('GROQ_KEY')

def health_benefits(fruit):
        client = Groq(api_key=api_key)
        schema = {'benefit': 'detailed explanation'}
        # to prevent a break, i will return none if agent encounters an error.
        try:
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                        {
                            "role": "system",
                            "content": f"You are a program that returns this kind of JSON schema {schema}"
                        },
                        {
                            "role": "user",
                            "content": f"Give me the health benefits of a fruit such as {fruit}"
                        },
                ],
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False,
                response_format={"type": "json_object"},
                stop=None,
            )
            benefits = response.choices[0].message.content
            benefits = json.loads(benefits)
            # --------------------------------------------------
            # print(type(benefits))
            # num = 0
            # for key, value in benefits.items():
            #         num += 1
            #         print('title: ', key, '\n')
            #         print('content: ', value)
            #         print(num)
            # --------------------------------------------------
            return benefits
        
        except:
              return None