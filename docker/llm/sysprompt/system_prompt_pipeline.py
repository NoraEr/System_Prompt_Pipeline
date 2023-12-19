import yaml
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
    
from . import current_dir
import os

class BuildPrompt:
    def __init__(self,filename):
        with open(filename, 'r') as f:
            self.prompt_template = "".join([line.replace('\n','') for line in f.readlines()])

    def build_prompt(self, parameters_dict):
        prompt_text= self.prompt_template
        for param in parameters_dict.keys():
            prompt_text = prompt_text.replace('{'+ param +'}', parameters_dict[param])
        return prompt_text

class PromptPipeline:
    def __init__(self, filename= current_dir+ '/system_prompt_values.yaml'):
        with open(filename, 'r') as stream:
            self.yaml_dict = yaml.load(stream, Loader)

    def yaml_to_prompt(self):
        prompts= []
        template_directory = os.path.join(current_dir, self.yaml_dict['metadata']['template_directory'])
        prompt_pipeline = self.yaml_dict['prompt_pipeline']
        for prompt_type in prompt_pipeline.keys():
            prompt_params = prompt_pipeline[prompt_type]
            filename = prompt_params['filename']
            abs_path_filename = template_directory + '/' + filename
            parameters_dict = prompt_params.get('parameters', None)

            if parameters_dict is not None:
                prompts.append(BuildPrompt(abs_path_filename).build_prompt(parameters_dict))
            else:
                prompts.append(BuildPrompt(abs_path_filename).prompt_template)
        
        prompt_text = " ".join(prompts)
        return prompt_text
    
    @staticmethod
    def save_prompt(prompt_text):
        prompt_text = prompt_text.replace('. ', '.\n')
        with open(current_dir+ '/output_system_prompt.txt', 'w') as f:
            f.write(prompt_text)