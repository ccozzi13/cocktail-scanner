from google import genai
from google.genai.types import HttpOptions, Part
import configparser
from io import BytesIO
from PIL import Image
import pillow_heif

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

def generate_invent_text_prompt(schema_prompt, additional_prompts, json_prompt, bar_assistant_schema, invent_prompt, invent_text):
    full_prompt = (schema_prompt +
                   additional_prompts +
                   json_prompt +
                   bar_assistant_schema +
                   invent_prompt +
                   invent_text)
    return full_prompt

def generate_image_prompt(schema_prompt, additional_prompts, json_prompt, bar_assistant_schema):
    full_prompt = (schema_prompt +
                   additional_prompts +
                   json_prompt +
                   bar_assistant_schema)
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

def get_model_response_image(api_key, model_name, prompt, image, image_type):
    if api_key is None:
        print("Error: Google API key is not provided.")
        return None

    client = genai.Client(api_key=api_key)
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=[
                prompt,
                Part.from_bytes(data=image,mime_type=image_type)
            ]
        )
        return response.text
    except Exception as e:
        print(f"Error during model interaction: {e}")
        return None


def convert_heic_to_png(heic_bytes):
    try:
        heif_file = pillow_heif.open_heif(heic_bytes)
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )

        png_bytes = BytesIO()
        image.save(png_bytes, format="PNG")
        return png_bytes.getvalue()
    except Exception as e:
        raise Exception(f"Error converting HEIC to PNG: {e}")





