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

col1, col2, col3 = st.columns(3)

with col1:
    st.write("Where did you source this recipe? Select and existing source, or enter a new one.")

    sources = sorted(cocktail_scanner_parameters.common_sources)
    source_select  = st.selectbox("Common sources", sources, index=None, label_visibility="collapsed")

    source_raw = st.text_input("Source", " ", key='source_raw', label_visibility="collapsed")

    if source_select:
        source = source_select
    else:
        source = source_raw

with col2:
    st.write("Upload an image:")

    uploaded_file = st.file_uploader(
        "Upload an image", accept_multiple_files=False, type=["jpg", "jpeg", "png", "heic"], label_visibility="collapsed"
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

with col3:
    st.write("Or upload cocktail recipe or simple description:")

    @st.dialog("Enter a cocktail recipe", width="large")
    def cocktail_text():
        cocktail_text_submitted = st.text_area("Cocktail recipe", height=400, label_visibility="visible")
        if st.button("Submit",key='cocktail_text_submit'):
            st.session_state.cocktail_text = {"submitted_text": cocktail_text_submitted}
            st.rerun()

    if "cocktail_text" not in st.session_state:
        if st.button("Upload cocktail recipe",key='cocktail_text_no_text'):
            cocktail_text()
    else:
        if st.button("Re-upload cocktail recipe",key='cocktail_text_replace_text'):
            cocktail_text()

    @st.dialog("Enter a cocktail description", width="large")
    def cocktail_desc():
        cocktail_desc_submitted = st.text_area("Cocktail description", height=400, label_visibility="visible")
        if st.button("Submit",key='cocktail_desc_submit'):
            st.session_state.cocktail_desc = {"submitted_text": cocktail_desc_submitted}
            st.rerun()

    if "cocktail_desc" not in st.session_state:
        if st.button("Upload cocktail description",key='cocktail_desc_no_text'):
            cocktail_desc()
    else:
        if st.button("Re-upload cocktail description",key='cocktail_desc_replace_text'):
            cocktail_desc()

st.header("Review Data", divider="blue")

if "cocktail_text" in st.session_state:
    st.write("Submitted text:")
    st.code(st.session_state.cocktail_text['submitted_text'], language=None, line_numbers=False, wrap_lines=True, height=250)
elif "cocktail_image" in st.session_state:
    st.image(st.session_state.cocktail_image['cocktail_image'], caption="Submitted image")
if "cocktail_desc" in st.session_state:
    st.write("Submitted text:")
    st.code(st.session_state.cocktail_desc['submitted_text'], language=None, line_numbers=False, wrap_lines=True, height=250)
else:
    st.badge("No data submitted yet!", icon=":material/info:", color="blue")

if "cocktail_text" in st.session_state:
    #st.write("Submitted prompt:")
    st.session_state.prompt = {"prompt": cocktail_scanner_ai.generate_full_text_prompt(cocktail_scanner_parameters.schema_text_prompt,
                                                      cocktail_scanner_parameters.additional_prompts,
                                                      cocktail_scanner_parameters.json_prompt,
                                                      cocktail_scanner_parameters.bar_assistant_schema,
                                                      cocktail_scanner_parameters.recipe_prompt,
                                                      st.session_state.cocktail_text['submitted_text']+"The source of this recipe was: "+source)}
    #st.code(st.session_state.prompt['prompt'], language=None, line_numbers=False, wrap_lines=True, height=250)
elif "cocktail_image" in st.session_state:
    #st.write("Submitted prompt:")
    st.session_state.prompt = {"prompt": cocktail_scanner_ai.generate_image_prompt(cocktail_scanner_parameters.schema_image_prompt,
                                                      cocktail_scanner_parameters.additional_prompts,
                                                      cocktail_scanner_parameters.json_prompt,
                                                      cocktail_scanner_parameters.bar_assistant_schema+"The source of this recipe was: "+source),
                               "invent_prompt": cocktail_scanner_ai.generate_image_prompt(
                                   cocktail_scanner_parameters.schema_invent_prompt,
                                   cocktail_scanner_parameters.additional_prompts,
                                   cocktail_scanner_parameters.json_prompt,
                                   cocktail_scanner_parameters.bar_assistant_schema + "The source of this recipe was: " + source)
                               }
    #st.code(st.session_state.prompt['prompt'], language=None, line_numbers=False, wrap_lines=True, height=250)
elif "cocktail_desc" in st.session_state:
    #st.write("Submitted prompt:")
    st.session_state.prompt = {"prompt": cocktail_scanner_ai.generate_full_text_prompt(cocktail_scanner_parameters.schema_invent_prompt,
                                                      cocktail_scanner_parameters.additional_prompts,
                                                      cocktail_scanner_parameters.json_prompt,
                                                      cocktail_scanner_parameters.bar_assistant_schema,
                                                      cocktail_scanner_parameters.invent_prompt,
                                                      st.session_state.cocktail_desc['submitted_text']+"The source of this recipe was: "+source)}
    #st.code(st.session_state.prompt['prompt'], language=None, line_numbers=False, wrap_lines=True, height=250)
else:
    #st.badge("No data submitted yet!", icon=":material/info:", color="blue")
    pass

st.header("Model Output", divider="blue")

col_m, buff_m = st.columns([1, 5])

with col_m:
    models = sorted(cocktail_scanner_parameters.all_models)
    selected_model = st.selectbox("Select a model:", models, label_visibility="visible")

with st.container(height=400, border=False):

    if "cocktail_text" in st.session_state:
        if st.button("Submit a recipe", key='submit_text_prompt'):
            google_key = cocktail_scanner_ai.get_google_api_key('local.ini', 'API', 'google_key')
            st.session_state.model_response = {"model_response": cocktail_scanner_ai.get_model_response(google_key, selected_model, st.session_state.prompt['prompt'])}
    elif "cocktail_image" in st.session_state:
        if st.button("Submit an image recipe", key='submit_image_prompt'):
            google_key = cocktail_scanner_ai.get_google_api_key('local.ini', 'API', 'google_key')
            st.session_state.model_response = {"model_response": cocktail_scanner_ai.get_model_response_image(google_key, selected_model, st.session_state.prompt['prompt'],st.session_state.cocktail_image['cocktail_image'],st.session_state.cocktail_image['image_type'])}
        if st.button("Submit an image description", key='submit_invent_image_prompt'):
            google_key = cocktail_scanner_ai.get_google_api_key('local.ini', 'API', 'google_key')
            st.session_state.model_response = {"model_response": cocktail_scanner_ai.get_model_response_image(google_key, selected_model, st.session_state.prompt['invent_prompt'],st.session_state.cocktail_image['cocktail_image'],st.session_state.cocktail_image['image_type'])}
    elif "cocktail_desc" in st.session_state:
        if st.button("Generate a recipe", key='submit_invent_text_prompt'):
            google_key = cocktail_scanner_ai.get_google_api_key('local.ini', 'API', 'google_key')
            st.session_state.model_response = {"model_response": cocktail_scanner_ai.get_model_response(google_key, selected_model, st.session_state.prompt['prompt'])}

    if "model_response" in st.session_state:
        st.write("Review and copy this JSON to BarAssistant:")
        #st.code(st.session_state.model_response['model_response'], language=None, line_numbers=False, wrap_lines=True, height=250)
        st.markdown(st.session_state.model_response['model_response'])
    else:
        st.badge("No data submitted yet!", icon=":material/info:", color="blue")

#with st.expander("Debugging data"):
    #st.code(cocktail_scanner_parameters.bar_assistant_schema, language="css", height=200)
