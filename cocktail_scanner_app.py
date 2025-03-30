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

st.write("Where did you source this recipe? Select and existing source, or enter a new one.")

col_source1, col_source2 = st.columns(2)

with col_source1:
    sources = sorted(cocktail_scanner_parameters.common_sources)
    source_select  = st.selectbox("Common sources", sources, index=None)

with col_source2:
    source_raw = st.text_input("Source", " ", key='source_raw')

if source_select:
    source = source_select
else:
    source = source_raw

st.write(source)

col1, col2 = st.columns(2)

with col2:
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


with col1:
    uploaded_file = st.file_uploader(
        "Upload an image", accept_multiple_files=False, type=["jpg", "jpeg", "png", "heic"]
    )
    if uploaded_file is not None:
        if uploaded_file.type == 'application/octet-stream':
            file_bytes = cocktail_scanner_ai.convert_heic_to_png(uploaded_file.getvalue())
            file_type = 'image/png'
        else:
            file_bytes = uploaded_file.getvalue()
            file_type = uploaded_file.type
        st.session_state.cocktail_image = {"cocktail_image": file_bytes, "image_type": file_type}
        #st.write(st.session_state.cocktail_image['image_type'])

#with col3:
#    @st.dialog("Paste the text from a cocktail recipe")
#    def cocktail_camera():
#        cocktail_camera_submitted = st.text_input("Recipe text...")
#        if st.button("Submit",key='cocktail_camera_submit'):
#            st.session_state.cocktail_camera = {"cocktail_camera": cocktail_camera_submitted}
#            st.rerun()

#    if "cocktail_camera" not in st.session_state:
#        if st.button("Take a photo",key='cocktail_camera_no_image'):
#            cocktail_camera()
#    else:
#        f"Text submitted"

st.header("Review Data & Prompt", divider="blue")

col4, col5 = st.columns(2)

with col4:
    if "cocktail_text" in st.session_state:
        st.write("Submitted text:")
        st.code(st.session_state.cocktail_text['submitted_text'], language=None, line_numbers=False, wrap_lines=True, height=250)
    elif "cocktail_image" in st.session_state:
        st.image(st.session_state.cocktail_image['cocktail_image'], caption="Submitted image")
    else:
        st.badge("No data submitted yet!", icon=":material/info:", color="blue")

with col5:
    if "cocktail_text" in st.session_state:
        st.write("Submitted prompt:")
        st.session_state.prompt = {"prompt": cocktail_scanner_ai.generate_full_text_prompt(cocktail_scanner_parameters.schema_text_prompt,
                                                          cocktail_scanner_parameters.additional_prompts,
                                                          cocktail_scanner_parameters.json_prompt,
                                                          cocktail_scanner_parameters.bar_assistant_schema,
                                                          cocktail_scanner_parameters.recipe_prompt,
                                                          st.session_state.cocktail_text['submitted_text']+"The source of this recipe was: "+source)}
        st.code(st.session_state.prompt['prompt'], language=None, line_numbers=False, wrap_lines=True, height=250)
    elif "cocktail_image" in st.session_state:
        st.write("Submitted prompt:")
        st.session_state.prompt = {"prompt": cocktail_scanner_ai.generate_image_prompt(cocktail_scanner_parameters.schema_image_prompt,
                                                          cocktail_scanner_parameters.additional_prompts,
                                                          cocktail_scanner_parameters.json_prompt,
                                                          cocktail_scanner_parameters.bar_assistant_schema+"The source of this recipe was: "+source)}
        st.code(st.session_state.prompt['prompt'], language=None, line_numbers=False, wrap_lines=True, height=250)
    else:
        #st.badge("No data submitted yet!", icon=":material/info:", color="blue")
        pass

st.header("Model Output", divider="blue")

with st.container(height=400, border=False):
    if "cocktail_text" in st.session_state:
        if st.button("Submit text prompt", key='submit_text_prompt'):
            google_key = cocktail_scanner_ai.get_google_api_key('local.ini', 'API', 'google_key')
            st.session_state.model_response = {"model_response": cocktail_scanner_ai.get_model_response(google_key, cocktail_scanner_parameters.default_model, st.session_state.prompt['prompt'])}
    elif "cocktail_image" in st.session_state:
        if st.button("Submit image prompt", key='submit_image_prompt'):
            google_key = cocktail_scanner_ai.get_google_api_key('local.ini', 'API', 'google_key')
            st.session_state.model_response = {"model_response": cocktail_scanner_ai.get_model_response_image(google_key, cocktail_scanner_parameters.default_model, st.session_state.prompt['prompt'],st.session_state.cocktail_image['cocktail_image'],st.session_state.cocktail_image['image_type'])}

    if "model_response" in st.session_state:
        st.write("Review and copy this JSON to BarAssistant:")
        #st.code(st.session_state.model_response['model_response'], language=None, line_numbers=False, wrap_lines=True, height=250)
        st.markdown(st.session_state.model_response['model_response'])
    else:
        st.badge("No data submitted yet!", icon=":material/info:", color="blue")

#with st.expander("Debugging data"):
    #st.code(cocktail_scanner_parameters.schema_prompt, height=200)
    #st.code(cocktail_scanner_parameters.additional_prompts, height=200)
    #st.code(cocktail_scanner_parameters.bar_assistant_schema, language="css", height=200)