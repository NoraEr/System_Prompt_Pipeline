# Improved structure and readability of your LLM system prompt

Azure OpenAI service has published a [system message framework](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/system-message). System prompts fed into LLM's such as Openai GPT models can be used to guide an AI system’s behavior and improve system performance. Azure system message framework consists of four **categories**:
- **Tasks**: Define the model’s tasks, capabilities and limitations
- **Format**: Define the model’s output format
- **Examples**: Provide examples to demonstrate the intended behavior of the model
- **Guardrails**    : Provide additional behavioral guardrails  

This project helps you structure your system prompt using the Azure system message framework.
The system prompt is broken down into four prompts following the recommended **categories** as highlighted above. A YAML configuration file declares the pipeline for the system prompts by defining the prompt for each category. 

## Re-usable system prompts for different use cases
You may need to design a common system prompt for different use cases.
For example, you have built a chatbot for customer service support that answers questions about product X. You want to re-use the same code and prompts to build a chatbot that answer questions about product Y.
Without changing the prompt itself, you can simply change the parameter in the YAML configuration file.
The same prompt defined in `system_prompt_tasks.txt`` below would apply to both use cases:
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

The code is containerised using Docker. 

- Define your user prompt in `llm/user_prompt.txt`
- Inside `docker` folder, build the image using:
``` docker build -t <image_name> -f Dockerfile . ```
- Run the image using: ```docker run <image_name>```
  This prints the output from the LLM in the terminal.

## Code structure

### System prompts

The module `llm/sysprompts` defines the system prompt templates:

- System prompts for the four **categories** are defined in `llm/sysprompt/templates`
- The yaml files which contains the system prompt pipelines and values for prompt parameters, is defined in `llm/sysprompt/system_prompt_values.yaml`
- Unit tests for the system prompt are defined in `llm/tests` and are run using pytest.
- when running the Docker image, the overall final system prompt is saved in `llm/sysprompt/output_system_prompt.txt`

### LLM inference

The module `llm/inference` defines the inference call to OpenAI API service.
Inside this module, you should define your Openai API key, the model name and other model parameters in the `.env` file

