import os
from dotenv import load_dotenv
import openai
import logging

load_dotenv()

api_key = os.environ.get('OPENAI_API_KEY')


class Completion:
    """
    A class for interacting with the OpenAI GPT chat completions API.

    Attributes:
    - client: object
              An instance of the OpenAI API client.
    - model:  str
              The GPT model identifier.
    - temperature:  float
                    The temperature parameter for controlling the randomness of responses.

    Methods:
    - __init__: Initializes the Completion object with the OpenAI API client, model, and temperature.
    - verify_api_key: Static method to verify that the OpenAI API key is defined.
    - verify_user_prompt: Static method to verify that the user prompt is defined.
    - request_response: Sends a request to the OpenAI API for chat completion and prints the response.

    Usage:
    completion = Completion()
    completion.request_response(user_prompt, system_prompt)
    """
    def __init__(self):
        """
        Initializes the Completion object.

        Attributes:
        - client: object
                An instance of the OpenAI API client.
        - model:  str
                The GPT model identifier.
        - temperature:  float
                        The temperature parameter for controlling the randomness of responses.
        """
        self.client = openai.OpenAI(api_key=api_key)
        self.model = os.environ.get('model')
        self.temperature = float(os.environ.get('temperature'))
    
    @staticmethod
    def verify_api_key():
        """
        Static method to verify that the OpenAI API key is defined.
        Raises AssertionError and exits the program if the key is not defined.
        """
        try:
            assert api_key !=""
            return api_key
        except AssertionError:
            logging.error('OPENAI API KEY is not defined. Please enter your API KEY in .env file')
            return None


    @staticmethod
    def verify_user_prompt(user_prompt):
        """
        Static method to verify that the user prompt is not empty.
        Raises AssertionError and exits the program if the prompt is empty.

        Parameters:
        - user_prompt: str
                       The user prompt to be verified.
        """
        try:
            assert user_prompt.strip() !=""
            return user_prompt
        except AssertionError:
            logging.error('User prompt must be non empty. Please enter your prompt in user_prompt.txt file')
            return None

    def request_response(self, user_prompt, system_prompt):
        """
        Sends a request to the OpenAI API for chat completion and prints the response.

        Parameters:
        - user_prompt: str
                       The user's input prompt for the chat.
        - system_prompt: str
                         The system's input prompt for the chat.
        
        Returns:
        - response: str
                    response generatedy OpenAI API model
        """
        api_key_check = self.verify_api_key()
        user_prompt_check = self.verify_user_prompt(user_prompt)

        if api_key_check == None or user_prompt_check == None:
            return None

        try:
            completion = self.client.chat.completions.create(
            model = self.model,
            temperature= self.temperature,
            messages=[
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": f"{user_prompt}"}])
            response = completion.choices[0].message.content
            return response
    
        except openai.AuthenticationError as error:
            logging.error(f"Invalid Openai API key: {error}")
            return None
        except openai.RateLimitError as error:
            logging.error(f"Too many requests: {error}")
            return None
        except openai.APIConnectionError as error:
            logging.error(f"API connection error: {error}")
            return None
        except openai.APITimeoutError as error:
            logging.error(f"API timeout error: {error}")
            return None
        except openai.BadRequestError as error:
            logging.error(f"Bad request error: {error}")
            return None
        except openai.ConflictError as error:
            logging.error(f"Conflict error: {error}")
            return None
        except openai.InternalServerError as error:
            logging.error(f"Internal server error: {error}")
            return None
        except openai.NotFoundError as error:
            logging.error(f"Request resource not found: {error}")
            return None
        except openai.PermissionDeniedError as error:
            logging.error(f"Permission denied: {error}")
            return None
        except openai.UnprocessableEntityError as error:
            logging.error(f"Unable to process request: {error}")
            return None


    

