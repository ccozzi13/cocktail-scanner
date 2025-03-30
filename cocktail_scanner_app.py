#Libraries
import streamlit as st
import pandas as pd

import cocktail_scanner_parameters
import cocktail_scanner_ai

#Application Config
st.set_page_config(
    page_title="Cocktail Scanner",
    layout="wide",
    initial_sidebar_state="expanded"
)

#Application
st.title("Cocktail Scanner")
st.write("Convert cocktail recipe text, images or cell phone snaps to BarAssistant import format.")

st.header("Import Data", divider="blue")
st.write("Where did you source this recipe?")

source = st.text_input("Source", " ")

col1, col2, col3 = st.columns(3)

with col1:
    @st.dialog("Paste the text from a cocktail recipe", width="large")
    def cocktail_text():
        cocktail_text_submitted = st.text_area("Cocktail recipe", height=400, label_visibility="visible")
        if st.button("Submit",key='cocktail_text_submit'):
            st.session_state.cocktail_text = {"submitted_text": cocktail_text_submitted}
            st.rerun()

    if "cocktail_text" not in st.session_state:
        if st.button("Upload recipe text",key='cocktail_text_no_text'):
            cocktail_text()
    else:
        if st.button("Re-upload recipe text",key='cocktail_text_replace_text'):
            cocktail_text()



with col2:
    @st.dialog("Upload an image")
    def cocktail_image():
        cocktail_image_submitted = st.text_input("Recipe text...")
        if st.button("Submit",key='cocktail_image_submit'):
            st.session_state.cocktail_image = {"cocktail_image": cocktail_image_submitted}
            st.rerun()

    if "cocktail_image" not in st.session_state:
        if st.button("Upload an image",key='cocktail_image_no_image'):
            cocktail_image()
    else:
        f"Text submitted"

with col3:
    @st.dialog("Paste the text from a cocktail recipe")
    def cocktail_camera():
        cocktail_camera_submitted = st.text_input("Recipe text...")
        if st.button("Submit",key='cocktail_camera_submit'):
            st.session_state.cocktail_camera = {"cocktail_camera": cocktail_camera_submitted}
            st.rerun()

    if "cocktail_camera" not in st.session_state:
        if st.button("Take a photo",key='cocktail_camera_no_image'):
            cocktail_camera()
    else:
        f"Text submitted"

st.header("Review Data & Prompt", divider="blue")

col4, col5 = st.columns(2)

with col4:
    if "cocktail_text" in st.session_state:
        st.write("Submitted text:")
        st.code(st.session_state.cocktail_text['submitted_text'], language=None, line_numbers=False, wrap_lines=True, height=250)
    else:
        st.badge("No data submitted yet!", icon=":material/info:", color="blue")

with col5:
    if "cocktail_text" in st.session_state:
        st.write("Submitted prompt:")
        st.session_state.prompt = {"prompt": cocktail_scanner_ai.generate_full_text_prompt(cocktail_scanner_parameters.schema_prompt,
                                                          cocktail_scanner_parameters.additional_prompts,
                                                          cocktail_scanner_parameters.json_prompt,
                                                          cocktail_scanner_parameters.bar_assistant_schema,
                                                          cocktail_scanner_parameters.recipe_prompt,
                                                          st.session_state.cocktail_text['submitted_text']+"The source of this recipe was: "+source)}
        st.code(st.session_state.prompt['prompt'], language=None, line_numbers=False, wrap_lines=True, height=250)
    else:
        #st.badge("No data submitted yet!", icon=":material/info:", color="blue")
        pass

st.header("Model Output", divider="blue")

with st.container(height=400, border=False):
    if "cocktail_text" in st.session_state:
        if st.button("Submit prompt", key='submit_text_prompt'):
            google_key = cocktail_scanner_ai.get_google_api_key('local.ini', 'API', 'google_key')
            st.session_state.model_response = {"model_response": cocktail_scanner_ai.get_model_response(google_key, cocktail_scanner_parameters.default_model, st.session_state.prompt['prompt'])}

    if "model_response" in st.session_state:
        st.write("Review and copy this JSON to BarAssistant:")
        #st.code(st.session_state.model_response['model_response'], language=None, line_numbers=False, wrap_lines=True, height=250)
        st.markdown(st.session_state.model_response['model_response'])
    else:
        st.badge("No data submitted yet!", icon=":material/info:", color="blue")

with st.expander("Debugging data"):
    st.code(cocktail_scanner_parameters.schema_prompt, height=200)
    st.code(cocktail_scanner_parameters.additional_prompts, height=200)
    st.code(cocktail_scanner_parameters.bar_assistant_schema, language="css", height=200)

    #google_key = cocktail_scanner_api.get_google_api_key()

    #if google_key:
        # Generate the full prompt

     #   print("Full prompt generated in the main script:")
      #  print(prompt)

        # Get the model response
       # model_output = cocktail_scanner_api.get_model_response(google_key, prompt=prompt)

        #if model_output:
         #   print("Model output received in the main script:")
            # Process the model_output as needed
    #else:
     #   print("Could not retrieve Google API key. Exiting.")