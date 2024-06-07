import streamlit as st
from PIL import Image

#configurando horizontalmente a pagina
st.set_page_config(page_title="Home",page_icon='🏠', layout="wide")

image_path ='zomato_logo.png'
image = Image.open(image_path)
st.sidebar.image( image, width =280)

#titulo sidebar
st.sidebar.markdown('# Zomato - Food Delivery')
st.sidebar.markdown('## The Best Restaurant for You')
st.sidebar.markdown("""---""")

#assinatura
st.sidebar.markdown('#### Desenvolvido por Samuel Lima')

st.title(' Zomato Dashboards.')
st.divider()

st.markdown ( '### Seja bem vindo ao Dashboard Interativo da Zomato')
st.markdown( ' O objetivo da criação deste Dashboard é para fornecer as métricas de acompanhamento e crescimento solicitadas pelo CEO, afim de que possa tomar as melhores decisões estratégicas para a Empresa.')
st.markdown("""---""")

st.markdown ( '### Sobre a Zomato')
st.markdown( ' A Zomato é um serviço de busca de restaurantes para quem quer sair para jantar, buscar comida ou pedir em casa e esta localizada em mais de 10 Países e mais de 100 cidades cadastradas em sua plataforma.')

st.markdown("""---""")
st.markdown ( '### Como utilizar o Zomato Dashboards:')
st.markdown( ' Este Dashboard possui, além desta aqui, 3 abas. Que se refere a:')

st.markdown ( '##### - Visão Geral:')
st.markdown ( 'Informaçoes sobre métricas gerais da Zomato e a localização dos Restaurantes parceiros.')

st.markdown ( '##### - Dashboards:')
st.markdown ( 'Contêm Dashboards interativos com métricas dos países, cidades,restaurantes e culinárias.')

st.markdown ( '##### - Contatos:')
st.markdown ( 'Principais formas de entrar em contato comigo.')






