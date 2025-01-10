import streamlit as st
from backend import obter_transcricao_youtube, get_language_data

st.title('YouTube Video Transcriber')

# Carregar dados de idioma
languages = get_language_data()

# Criar lista para dropdown
options = [
    (lang['portuguese_br_name'], lang['country_flag_url'], lang['language_country_name']) 
    for lang in languages
]

# Entrada de dados
video_id = st.text_input('Enter YouTube Video ID:')
video_lang = st.selectbox(
   'Select video language:', 
   options,
   format_func=lambda x: f"{x[2]} - {x[0]}")
trans_lang = st.selectbox(
  'Select transcription language:', 
   options,
   format_func=lambda x: f"{x[2]} - {x[0]}")

# Exibir bandeira do país selecionado
st.image(video_lang[1], width=20)

# Botão para obter transcrição
if st.button('Transcribe Video'):
    transcription = obter_transcricao_youtube(video_id, video_lang, trans_lang)
    st.text_area("Transcription:", value=transcription, height=300)

# Rodar o app: streamlit run app.py
