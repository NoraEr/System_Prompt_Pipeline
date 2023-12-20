# Improve structure and readability of your LLM system prompt

## Overall functionality of the code

The code builds the system prompt based on prompt templates and a configuration file.
Based on the system prompt as well as a user prompt, it sends a request to OpenAI API service. The code is containerised using Docker.

## Motivation for this project
Azure OpenAI service has published a [system message framework](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/system-message). System prompts fed into LLM's such as Openai GPT models can be used to guide an AI system’s behavior and improve system performance. Azure system message framework consists of four **categories**:
- **Tasks**: Define the model’s tasks, capabilities and limitations
- **Format**: Define the model’s output format
- **Examples**: Provide examples to demonstrate the intended behavior of the model
- **Guardrails**    : Provide additional behavioral guardrails  

**This project helps you better structure your system prompt using the Azure system message framework and improves readability especially with long complex system prompts.**

The system prompt is broken down into four prompts following the recommended **categories** as highlighted above. A YAML configuration file declares the pipeline for the system prompt by defining the prompt for each category and values for prompt parameters which can be easily modified. This layout has been inspired by Kubernetes Helm charts.

## Re-usable system prompts for different use cases
You may need to design a standard system prompt and adjust it for different use cases.
For example, you have built a chatbot for customer service support that answers questions about product X. You want to re-use the same code and prompts to build a chatbot that answer questions about a different product Y.
Without changing the prompt itself, you can simply change the product name in the YAML configuration file.
The same prompt defined in `system_prompt_tasks.txt` below would apply to both use cases:
```
You can only answer questions about product {product name}
```

In the YAML configuration file, you can change the value of the parameter `product name` from X to Y
```
prompt_pipeline:
    tasks: 
    filename: "system_prompt_tasks.txt"
    parameters:
      product name: Y
```

## How to run the code

The code is containerised using Docker and can be found in `docker` folder. 

- Define your user prompt in `llm/user_prompt.txt`
- Inside `docker` folder, build the image using:
``` docker build -t <image_name> -f Dockerfile . ```
- Run the image using: ```docker run <image_name>```
  This prints the system prompt, user prompt as well as OPENAI API response in the terminal.

## Code structure

### System prompts

The sub-module `llm/sysprompts` within `docker` defines the system prompt templates:

- System prompts for the four **categories** are defined in `llm/sysprompt/templates`
- The YAML configuration file which contains the system prompt pipelines and values for prompt parameters, is defined in `llm/sysprompt/system_prompt_values.yaml`
- Unit tests for the system prompt are defined at the root directory within `tests` and can be run using pytest. They also run automatically via the CI pipeline using Github Actions.

Example code:
```
from llm.sysprompt.system_prompt_pipeline import PromptPipeline
#build system prompt
prompt_pipeline = PromptPipeline()
system_prompt = prompt_pipeline.yaml_to_prompt()
#save system prompt for further inspection
prompt_pipeline.save_prompt(system_prompt)
```

### LLM inference

The module `llm/inference` defines the inference call to OpenAI API service and API error handling.
Inside this module, you should define your Openai API key, the model name and other model parameters in the `.env` file.
Please make sure to not commit any code with your Openai API key to Github.

