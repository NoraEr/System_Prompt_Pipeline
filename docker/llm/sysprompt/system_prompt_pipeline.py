import yaml
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
    
from . import current_dir
import os

class BuildPrompt:
    """
    A class for building prompts by replacing placeholders in a template with provided values.

    Attributes:
    - prompt_template: str
                       The template for the prompt read from a text file.

    Methods:
    - __init__: Initializes the BuildPrompt object with a template from a specified file.
    - build_prompt: Replaces placeholders in the template with values from a dictionary and returns the resulting prompt.

    Usage:
    build_prompt_instance = BuildPrompt('template.txt')
    prompt_parameters = {'param1': 'value1', 'param2': 'value2'}
    prompt_text = build_prompt_instance.build_prompt(prompt_parameters)
    """
    def __init__(self,filename):
        """
        Initializes the BuildPrompt object.

        Parameters:
        - filename:  str
                     The name of the text file containing the prompt template.
        """
        with open(filename, 'r') as f:
            self.prompt_template = "".join([line.replace('\n','') for line in f.readlines()])

    def build_prompt(self, parameters_dict):
        """
        Replaces placeholders in the template with values from a dictionary and returns the resulting prompt.

        Parameters:
        - parameters_dict: dict
                           A dictionary containing parameter-value pairs to replace in the template.

        Returns:
        - prompt_text: str
                       A string representing the prompt with placeholders replaced by corresponding values.
        """
        prompt_text= self.prompt_template
        for param in parameters_dict.keys():
            prompt_text = prompt_text.replace('{'+ param +'}', parameters_dict[param])
        return prompt_text

class PromptPipeline:
    """
    A class for processing a YAML configuration file and generating prompts based on specified templates.

    Attributes:
    - yaml_dict: dict
                 A dictionary loaded from a YAML configuration file containing prompt pipeline and parameters values.

    Methods:
    - __init__: Initializes the PromptPipeline object with a YAML configuration file.
    - yaml_to_prompt: Generates prompts based on specified templates and parameters from the YAML configuration.
    - save_prompt: Static method to save the generated prompt text to an output file.

    Usage:
    prompt_pipeline = PromptPipeline('config.yaml')
    generated_prompt = prompt_pipeline.yaml_to_prompt()
    PromptPipeline.save_prompt(generated_prompt)
    """
    def __init__(self, filename= current_dir+ '/system_prompt_values.yaml'):
        """
        Initializes the PromptPipeline object.

        Parameters:
        - filename: str
                    The name of the YAML configuration file containing prompt information.
                    Defaults to 'system_prompt_values.yaml' in the current directory.
        """
        with open(filename, 'r') as stream:
            self.yaml_dict = yaml.load(stream, Loader)

    def yaml_to_prompt(self):
        """
        Generates prompts based on specified templates and parameters from the YAML configuration.

        Returns:
        - prompt_text: str
                       A string representing the generated prompt.
        """
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
        """
        Static method to save the generated prompt text to an output file.

        Parameters:
        - prompt_text:  str
                        The text of the generated prompt to be saved.
        """
        prompt_text = prompt_text.replace('. ', '.\n')
        with open(current_dir+ '/output_system_prompt.txt', 'w') as f:
            f.write(prompt_text)