import logging

#Configure app logging for the entire package

#Create my app logger instance (to isolate this application logs from OpenAPI log)
#as we don't want to mix our application logs with OpenAI client logs
app_logger = logging.getLogger('system_prompt_application')
# Configure the app_logger separately from the root logger
#set severity level: any logging equal or above that level is permitted
app_logger.setLevel(logging.INFO)
#set logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#define and add handler to app logger (defines destination for saving logs and formatting)
handler = logging.StreamHandler() 
handler.setFormatter(formatter)
app_logger.addHandler(handler)