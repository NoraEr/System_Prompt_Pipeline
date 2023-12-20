from llm.sysprompt.system_prompt_pipeline import PromptPipeline
from llm.inference.chat_completion import Completion
import os

current_dir = os.path.dirname(__file__)

if __name__=="__main__":
    #build system prompt
    prompt_pipeline = PromptPipeline()
    system_prompt = prompt_pipeline.yaml_to_prompt()
    print("SYSTEM PROMPT:")
    print(f"{system_prompt}")
    #get user prompt
    with open(current_dir + '/user_prompt.txt', 'r') as f: 
        user_prompt = "".join([line.replace('\n','') for line in f.readlines()])
    print("USER PROMPT:")
    print(f"{user_prompt}")
    #request and print response from Openai API
    print("OPENAI API RESPONSE:")
    Completion().request_response(user_prompt, system_prompt)