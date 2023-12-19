import os
from dotenv import load_dotenv
import openai
import sys

load_dotenv()

api_key = os.environ.get('OPENAI_API_KEY')


class Completion:
    def __init__(self):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = os.environ.get('model')
        self.temperature = float(os.environ.get('temperature'))
    
    @staticmethod
    def verify_api_key():
        try:
            assert api_key !=""
        except AssertionError:
            print('OPENAI API KEY is empty. Please enter your API KEY in .env file')
            sys.exit(1)


    @staticmethod
    def verify_user_prompt(user_prompt):
        try:
            assert user_prompt.strip() !=""
        except AssertionError:
            print('User prompt must be non empty. Please enter your prompt in user_prompt.txt file')
            sys.exit(1)

    def request_response(self, user_prompt, system_prompt):
        self.verify_api_key()
        self.verify_user_prompt(user_prompt)

        try:
            completion = self.client.chat.completions.create(
            model = self.model,
            temperature= self.temperature,
            messages=[
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": f"{user_prompt}"}])
            response = completion.choices[0].message.content
            print(response)
    
        except openai.AuthenticationError as error:
            print('Invalid Openai API key:', error)
        except openai.RateLimitError as error:
            print('Too many requests:', error)
        except openai.APIConnectionError as error:
            print('API connection error:', error)
        except openai.APITimeoutError as error:
            print('API timeout error:', error)
        except openai.BadRequestError as error:
            print('Bad request error:', error)
        except openai.ConflictError as error:
            print('Conflict error:', error)
        except openai.InternalServerError as error:
            print('Internal server error:', error)
        except openai.NotFoundError as error:
            print('Request resource not found:', error)
        except openai.PermissionDeniedError as error:
            print('Permission denied:', error)
        except openai.UnprocessableEntityError as error:
            print('Unable to process request:', error)


    

