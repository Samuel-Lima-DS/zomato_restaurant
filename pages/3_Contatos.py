import streamlit as st
from PIL import Image

# ======================================================================
#BARRA LATERAL STREAMLIT
# ======================================================================

#configurando horizontalmente a pagina
st.set_page_config(page_title="Contatos",page_icon='📞', layout="wide")

#imagem
image_path ='zomato_logo.png'
image = Image.open(image_path)
st.sidebar.image(image , width = 120)

#titulo sidebar
st.sidebar.markdown('# Zomato - Food Delivery')
st.sidebar.markdown('## The Best Restaurant for You')
st.sidebar.markdown("""---""")

#assinatura
st.sidebar.markdown('#### Desenvolvido por Samuel Lima')

# =========================================================================
#LAYOUT STREAMLIT

st.title('📍 Onde você pode me encontrar:')
st.divider()
st.markdown( ' ### - Portfólio: ')
st.markdown( '#### https://samuel-lima-ds.github.io/portfolio_projetos/')
st.markdown( ' ### - Email: ')
st.markdown( '#### samuellimaesilva88@gmail.com')
st.markdown( ' ### - Linkedin: ')
st.markdown( '#### www.linkedin.com/in/samuellimaesilva/')
st.markdown( ' ### - Git Hub: ')
st.markdown( '#### www.github.com/Samuel-Lima-DS')
st.markdown( ' ### - Discord: ')
st.markdown( '#### @osamuellima')



