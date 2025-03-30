from google import genai
import configparser

def get_google_api_key(config_file, section, key_name):
    config = configparser.ConfigParser()
    config.read(config_file)
    try:
        return config[section][key_name]
    except KeyError:
        print(f"Error: Could not find '{key_name}' in section '{section}' of '{config_file}'.")
        return None

def generate_full_text_prompt(schema_prompt, additional_prompts, json_prompt, bar_assistant_schema, recipe_prompt, recipe_text):
    full_prompt = (schema_prompt +
                   additional_prompts +
                   json_prompt +
                   bar_assistant_schema +
                   recipe_prompt +
                   recipe_text)
    return full_prompt

def get_model_response(api_key, model_name, prompt):
    if api_key is None:
        print("Error: Google API key is not provided.")
        return None

    client = genai.Client(api_key=api_key)
    try:
        response = client.models.generate_content(model=model_name, contents=prompt)
        return response.text
    except Exception as e:
        print(f"Error during model interaction: {e}")
        return None









