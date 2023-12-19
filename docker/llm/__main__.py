from llm.sysprompt.system_prompt_pipeline import PromptPipeline
from llm.inference.chat_completion import Completion
import os

current_dir = os.path.dirname(__file__)

if __name__=="__main__":
    #build system prompt
    prompt_pipeline = PromptPipeline()
    system_prompt = prompt_pipeline.yaml_to_prompt()
    #save system prompt (makes sense to save user prompt also)
    prompt_pipeline.save_prompt(system_prompt)
    #get user prompt
    with open(current_dir + '/user_prompt.txt', 'r') as f: 
        user_prompt = "".join([line.replace('\n','') for line in f.readlines()])
    #request response from Openai model
    Completion().request_response(user_prompt, system_prompt)