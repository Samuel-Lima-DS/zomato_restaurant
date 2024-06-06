# Biblotecas
import inflection
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

#configurando horizontalmente a pagina
st.set_page_config(page_title="Geral",page_icon = '🌍',layout="wide")

#lendo dataset
dataframe = pd.read_csv('dataset/zomato.csv')

# ======================================================================
# Funcoes 
# ======================================================================

# Mapa =================================================================
def funcao_mapa (df):
    map = folium.Map([42 ,29], zoom_start=2)
    locations = list(zip(df.latitude, df.longitude))
    cluster = folium.plugins.MarkerCluster(locations=locations,popups=df['city'].tolist())  
    map.add_child(cluster)
    return map


# Renomear as colunas do data frame ====================================
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

# Criacao do nome das cores ===============================================
COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]


# Criação do tipo de Categoria de culinaria ================================
def create_price_tye(price_range):
    if price_range ==  1:
        return "cheap"
    elif price_range ==  2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"


# Preenchimento do Nome dos países ==========================================
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}
def country_name(country_id):
    return COUNTRIES[country_id]




# ======================================================================
# Tratamento dos dados
# ======================================================================

#renomeando colunas
df = rename_columns(dataframe)

#coluna de paises com função preenchimento dos nomes
df['country'] = df['country_code'].apply(country_name)

#tipo de categoria de comida 
df['price_range'] = df['price_range'].apply(create_price_tye)

#criação do nome das cores
df['rating_color'] = df['rating_color'].apply(color_name)

#nova coluna com a apenas um tipo de cozinha por restaurante
df['unique_cuisines'] = df['cuisines'].str.split(',', expand=True)[0]

#tratando nulo de uma coluna
df = df.loc[df['cuisines'].notna()]

#dropando nulos da coluna restaurant_id
df['restaurant_id'] = df['restaurant_id'].drop_duplicates()


# ======================================================================
#BARRA LATERAL STREAMLIT
# ======================================================================


st.title('Visão Geral')
st.markdown("""---""")

#imagem
image_path ='zomato_logo.png'
image = Image.open(image_path)
st.sidebar.image(image , width = 120)

#titulo sidebar
st.sidebar.markdown('# Zomato - Food Delivery')
st.sidebar.markdown('## The Best Restaurant for You')
st.sidebar.markdown("""---""")

#Filtros
st.sidebar.markdown (' ## Filtros')
country_options = st.sidebar.multiselect('Selecione os Países:',
                       ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'],
                       default=['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'])

st.sidebar.markdown("""---""")


#Interacao no FILTRO
linhas_selecionadas = df['country'].isin(country_options)
df = df.loc[linhas_selecionadas, :]

# Botão de Download

st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")

#Convertendo o dataframe em csv
csv = convert_df(df)

st.sidebar.markdown (' #### Dados utizados:')
st.sidebar.download_button(
    label="Download",
    data=csv,
    file_name="zomato.csv",
    mime="text/csv",
)

st.sidebar.markdown("""---""")
#assinatura
st.sidebar.markdown('#### Desenvolvido por Samuel Lima') 

# ======================================================================
#Layout Streamlit
# ======================================================================

#Colunas 
with st.container():
    st.markdown ('## Dados gerais.')
    col1, col2, col3, col4, col5 = st.columns(5 , gap = 'large')
    with col1:
        #Restaurantes Cadastrados
        rest_unico= df['restaurant_id'].nunique()
        col1.metric('Restaurantes cadastrados' , rest_unico)
        
    with col2:
        #Paises Cadastrados
        paises_unicos = len(df['country'].unique())
        col2.metric('Paises cadastrados',paises_unicos)
        
    with col3:
        #Cidades Cadastrados
        city_unico= df['city'].nunique()
        col3.metric('Cidades cadastradas', city_unico)

    with col4:
        # Total de avaliacoes
        total_avaliacao = df['votes'].sum()
        col4.metric('Avaliações realizadas' , total_avaliacao)

    with col5:
        # Tipos de culinarias disponiveis
        tipos_culin = len(df['unique_cuisines'].unique())
        col5.metric('Tipos de Culinárias',tipos_culin)

st.markdown("""---""")
st.markdown ('### Encontre nossos parceiros pelo mundo 🌏')
# Aplicando o mapa no layout 

map = funcao_mapa(df)
folium_static(map, width=1024, height=600)
        














