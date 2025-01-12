import streamlit as st
from backend import obter_transcricao_youtube, get_language_data
import logging
import utils

# Function to setup logger
def setup_logger():
    # Get the root logger
    logger = logging.getLogger()
    # Set the logging level
    logger.setLevel(logging.DEBUG)
    
    # Check if handlers are already configured
    if not logger.handlers:
        # Create a console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        
        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        
        # Add the handler to the logger
        logger.addHandler(ch)
    
    return logger

# Setup logger
logger = setup_logger()

st.title('YouTube Video Transcriber')

st.write(utils.validate_prereq())

# Carregar dados de idioma
languages = get_language_data()


# Criar lista para dropdown
options = [
    (lang['portuguese_br_name'], lang['country_flag_url'], lang['language_country_name']) 
    for lang in languages
]

# Pre-select the "Cherry" option. Indexing starts at 0, so Cherry is index 2.
default_index = options.index(('Português', 'https://flagcdn.com/16x12/br.png', 'Brasil'))
video_id_value=None
video_id_is_valid=False

# Initialize session state if not already done
if 'current_input' not in st.session_state:
    st.session_state.current_input = ""

def handle_text_input_change():
    # Retrieve the new input from Streamlit's session state
    new_input = st.session_state.video_id

    # Check if the input has changed to avoid redundant processing
    if new_input != st.session_state.get('current_input', ''):
        # Update the current input in session state
        st.session_state.current_input = new_input
        st.write(f"Input changed to: {new_input}")

        # Process the new input
        process_input(new_input)

def process_input(input_value):
    if utils.is_url(input_value):
        handle_url_input(input_value)
    else:
        handle_id_input(input_value)

def handle_url_input(url):
    logger.info('Input is a URL!')
    if utils.validate_url(url):
        video_id = utils.extract_video_id(url)
        if utils.validate_video_id(video_id):
            st.session_state.video_id_value = video_id
            st.session_state.video_id_is_valid = True
        else:
            st.session_state.video_id_is_valid = False
            st.error('O vídeo não é válido ou não foi localizado no YouTube.')
    else:
        logger.info('URL is invalid')
        st.warning('URL is invalid')
        st.session_state.video_id_is_valid = False

def handle_id_input(video_id):
    if utils.validate_video_id(video_id):
        st.session_state.video_id_value = video_id
        st.session_state.video_id_is_valid = True
    else:
        st.session_state.video_id_is_valid = False
        st.error('O vídeo não é válido ou não foi localizado no YouTube.')

# Entrada de dados
video_id = st.text_input('Enter YouTube Video ID or Url:', key='video_id', on_change=handle_text_input_change)
video_lang = st.selectbox(
   'Select video language:', 
   options,
   format_func=lambda x: f"{x[2]} - {x[0]}",
   index=default_index)

#validate_button = st.button("Validate")
#if validate_button:
#    st.text_input()

trans_lang = st.selectbox(
  'Select transcription language:', 
   options,
   format_func=lambda x: f"{x[2]} - {x[0]}",
   index=default_index)
   
# Exibir bandeira do país selecionado
st.image(video_lang[1], width=20)

# Botão para obter transcrição
if st.button('Transcribe Video'):
    transcription = obter_transcricao_youtube(video_id, video_lang, trans_lang)
    st.text_area("Transcription:", value=transcription, height=300)

# Rodar o app: streamlit run app.py
