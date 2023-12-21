from llm.sysprompt.system_prompt_pipeline import PromptPipeline
from llm.inference.chat_completion import Completion
import os
from . import app_logger

current_dir = os.path.dirname(__file__)

if __name__=="__main__":
    #build system prompt
    prompt_pipeline = PromptPipeline()
    system_prompt = prompt_pipeline.yaml_to_prompt()
    app_logger.info(f"SYSTEM PROMPT: {system_prompt}")
    #get user prompt
    with open(current_dir + '/user_prompt.txt', 'r') as f: 
        user_prompt = "".join([line.replace('\n','') for line in f.readlines()])
    app_logger.info(f"USER PROMPT: {user_prompt}")
    #request response from Openai API
    response = Completion().request_response(user_prompt, system_prompt)
    if response != None:
        app_logger.info(f"OPENAI API RESPONSE: {response}")