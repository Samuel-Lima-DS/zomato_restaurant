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
st.set_page_config(page_title="Dashboards",page_icon='📊', layout="wide")

#lendo dataset
dataframe = pd.read_csv('dataset/zomato.csv')

# ======================================================================
# Funcoes 
# ======================================================================

# Top restaurantes que fazem pedio online e entregas - Tab4 CUlinarias 
def top_culin_pedido_entrega (df):
    linhas = (df['has_online_delivery'] == 1) & (df['is_delivering_now'] == 1)
    colunas  = ['restaurant_id' , 'unique_cuisines']
    df_aux = df.loc[linhas,colunas].groupby('unique_cuisines').count().sort_values('restaurant_id' , ascending=False).reset_index()
    #renomeando coluna
    df_aux.columns=['Culinaria','Restaurantes']
    fig = df_aux.head(top_n)
    return fig

# Top culinarias por notas - Tab4 Culinarias 
def top_culin_notas (df):
    colunas = ['aggregate_rating' ,'unique_cuisines']
    df_aux = round(df.loc[:, colunas].groupby('unique_cuisines').mean().sort_values('aggregate_rating' , ascending=False).reset_index(),2)
    #acrescentar coluna
    df_aux['Avaliações'] = df['votes']
    #renomeando coluna
    df_aux.columns=['Culinaria','Nota Média','Avaliações Realizadas']
    fig = df_aux.head(top_n)
    return fig

# Percentual de restaurantes que faz reservas - Tab3 Restaurantes
def perc_rest_reserva (df):
    colunas = ['restaurant_id','has_table_booking']
    df_aux = df.loc[:,colunas].groupby('has_table_booking').count().reset_index()
    labels = ['Não faz Reserva' ,'Faz Reserva']
    fig = px.pie( df_aux, values='restaurant_id', names=labels, color_discrete_sequence=['red'], labels=labels)
    return fig 

# Percentual de restaurantes que faz entegas - Tab3 Restaurantes
def perc_rest_entregas (df):
    colunas = ['restaurant_id','has_online_delivery']
    df_aux = df.loc[:,colunas].groupby('has_online_delivery').count().reset_index()
    fig = px.pie( df_aux, values='restaurant_id', names=['Não Entregam' ,'Entregam'], color_discrete_sequence=['red'])
    return fig

# Top Restaurantes com melhores pratos - Tab3 Restaurantes
def top_rest_prato (df):
    colunas = ['average_cost_for_two' , 'restaurant_name', 'country']
    df_aux = (df.loc[: , colunas].groupby(['restaurant_name','country'])
                                 .max().sort_values('average_cost_for_two' , ascending =False).reset_index())
    #Renomeeando colunas
    df_aux.columns=['Restaurante' , 'País','Valor do prato para dois']
    fig=px.bar(df_aux.head(top_n) , x='Restaurante', y='Valor do prato para dois' , text ='Valor do prato para dois',color ='País')
    return fig 

# Top Restaurantes melhores avaliacoes - Tab3 Restaurantes
def top_rest_avaliacao (df):
    colunas = ['aggregate_rating' , 'restaurant_name']
    df_aux = df.loc[: , colunas].groupby('restaurant_name').mean().sort_values('aggregate_rating' , ascending =False).reset_index()
    #Renomeeando colunas
    df_aux.columns=['Restaurante' , 'Avaliação']
    fig = px.bar(df_aux.head(top_n) , x='Restaurante', y='Avaliação' , text ='Avaliação' , color='Restaurante')
    return fig

# Top cidades com restaurantes que possuem nota < 2.5  - Tab2 Cidades
def top_cidade_nota_abaixo_2meio (df):
    filtro = df['aggregate_rating'] < 2.5
    df_aux = (df.loc[filtro , ['restaurant_id','city','country' ]].groupby(['city','country'])
                                                    .count()
                                                    .sort_values('restaurant_id' , ascending =False)
                                                    .reset_index())
    df_aux.columns = ['Cidades','Paises','Restaurantes']
    fig = px.bar(df_aux.head(top_n), x='Cidades' , y='Restaurantes' , text='Restaurantes', color ='Paises')
    return fig

# Top cidades com restaurantes que possuem nota > 4 - Tab2 Cidades
def top_cidade_nota_acima_4 (df):
    filtro = df['aggregate_rating'] > 4
    df_aux = (df.loc[filtro , ['restaurant_id','city','country']]
                .groupby(['city','country'])
                .count()
                .sort_values('restaurant_id' , ascending =False)
                .reset_index())
    df_aux.columns = ['Cidades','Paises','Restaurantes']
    fig = px.bar(df_aux.head(top_n), x='Cidades' , y='Restaurantes' , text='Restaurantes', color ='Paises')
    return fig

# Top Cidades com mais Restaurantes - Tab2 Cidades
def qtd_rest_cidade (df):
    colunas = ['restaurant_id' , 'city']
    df_aux = df.loc[: , colunas].groupby('city').count().sort_values('restaurant_id', ascending = False).reset_index()
    #Renomear colunas
    df_aux.columns=['Cidades', 'Restaurantes']
    fig = px.bar(df_aux.head(top_n) , x ='Cidades' , y= 'Restaurantes', text='Restaurantes', color ='Cidades')
    return fig

# Top Paises com Melhor Avaliacao - Tab1 Paises
def top_pais_avaliacao (df):
    colunas = [ 'country' , 'aggregate_rating']
    df_aux = round(df.loc[: , colunas].groupby('country').mean().sort_values('aggregate_rating' , ascending =False).reset_index(),2)
    #Renomear colunas
    df_aux.columns=['Países','Avaliação']
    fig = px.bar(df_aux.head(top_n) , x='Países', y='Avaliação', text='Avaliação',color_discrete_sequence=['red'])
    return fig

# Top Países com mais tipos de CUlinarias - Tab1 Paises
def top_pais_culinarias (df):
    colunas = [ 'country' , 'unique_cuisines']
    df_aux = df.loc[: , colunas].groupby('country').nunique().sort_values('unique_cuisines' , ascending =False).reset_index()
    #Renomear Colunas
    df_aux.columns = ['Países' , 'Culinárias']
    fig = px.bar(df_aux.head(top_n) , x='Países', y='Culinárias' , text='Culinárias',color_discrete_sequence=['red'])
    return fig

# Top Restaurantes gourmet - Tab1 Paises
def top_rest_gourmet (df):
    linhas = df['price_range'] == 'gourmet'
    df_aux = (df.loc[ linhas, ['country', 'price_range']]
                        .groupby('country').count().sort_values('price_range' , ascending=False).reset_index())
    #Renomeando colunas 
    df_aux.columns = ['Países' , 'Restaurantes']
    fig = px.bar(df_aux.head(top_n) , x='Países', y='Restaurantes', text='Restaurantes',color_discrete_sequence=['red'])
    return fig

# Top Paises com mais cidades - Tab1 Paises
def top_pais_cidades (df):
    colunas = ['city' , 'country']
    df_aux = df.loc[: , colunas].groupby('country').nunique().sort_values('city' , ascending=False).reset_index()
    #Renomeando colunas 
    df_aux.columns = ['Países' , 'Cidades']
    fig = px.bar (df_aux.head(top_n) , x='Países' , y='Cidades', text ='Cidades',color_discrete_sequence=['red'])
    return fig

# Função Top Paises com Mais restaurantes - Tab1 Paises
def top_pais_rest (df):    
    colunas = ['restaurant_id' , 'country']
    df_aux = df.loc[: , colunas].groupby('country').count().sort_values('restaurant_id' , ascending=False).reset_index()
    #Renomeando colunas
    df_aux.columns =['Paises', 'Restaurantes']
    fig = px.bar (df_aux.head(top_n) , x='Paises' , y='Restaurantes', text ='Restaurantes',color_discrete_sequence=['red'])
    return fig

# Mapa 
def funcao_mapa (df):
    map = folium.Map([42 ,29], zoom_start=2)
    locations = list(zip(df.latitude, df.longitude))
    cluster = folium.plugins.MarkerCluster(locations=locations,popups=df['city'].tolist())  
    map.add_child(cluster)
    return map

# Renomear as colunas do data frame 
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

# Criacao do nome das cores 
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


# Criação do tipo de Categoria de culinaria 
def create_price_tye(price_range):
    if price_range ==  1:
        return "cheap"
    elif price_range ==  2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"


# Preenchimento do Nome dos países
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




#imagem
image_path ='zomato_logo.png'
image = Image.open(image_path)
st.sidebar.image(image , width = 120)

#titulo sidebar
st.sidebar.markdown('# Zomato - Food Delivery')
st.sidebar.markdown('## The Best Restaurant for You')
st.sidebar.markdown("""---""")

#Filtros

#Filtro para selecionar top melhores   
st.sidebar. markdown(' ## Filtros:')
    # Streamlit slider
top_n = st.sidebar.slider('Selecione o Top N que desejar', 1, 20, 10)
    
#    # Filter the top N items
df_aux = df
top_items = df_aux.head(top_n)

#Filtro para escolher países
country_options = st.sidebar.multiselect('Selecione os Países:',
                       ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'],
                       default=['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'])


# Botão de Download

@st.cache_data
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

#Interacao no FILTRO
linhas_selecionadas = df['country'].isin(country_options)
df = df.loc[linhas_selecionadas, :]


# ======================================================================
#Layout Streamlit
# ======================================================================

#Titulo 

st.title('📊 Dashboards')
st.markdown("""---""")

#Create tabs
tab1, tab2, tab3, tab4= st.tabs(['🌍 Países','🏙️ Cidades','🍽️ Restaurantes','🥗 Culinárias'])

with tab1:
    st.title( 'Visão Países 🌍')
    st.markdown("""---""")

    with st.container():
        col1, col2 = st.columns(2, gap='large')

        with col1:
            # Bar plot - Países com mais Restaurantes
            st.markdown(f'#### Top {top_n} Países com mais Restaurantes')
            fig = top_pais_rest(df)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Bar plot - Países com mais Cidades
            st.markdown(f'#### Top {top_n} Países com mais Cidades')
            fig = top_pais_cidades (df)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("""---""")
    with st.container():
        col1, col2 = st.columns(2 , gap='large')

        with col1:
            # Bar plot - Top Melhores Restaurantes Gourmet
            st.markdown( f'#### Top {top_n} Melhores Restaurantes da Categoria Gourmet')
            fig = top_rest_gourmet (df)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Bar plot -  Top Paises com mais CUlinárias 
            st.markdown (f' #### Top {top_n} Países com mais tipos de Culinárias')
            fig = top_pais_culinarias (df)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("""---""")
    with st.container():
        # Bar plot - Top Pais com melhor Avaliacao 
        st.markdown (f' #### Top {top_n} Países com a melhor nota média de Avaliação')
        fig = top_pais_avaliacao (df)
        st.plotly_chart(fig, use_container_width=True)

with tab2:

    with st.container():
        st.title( ' Visão Cidades 🏙️')
        st.markdown("""---""")    
 
        # Bar Plot - Quantidades de restaurante por cidades
        st.markdown(f' #### Top {top_n} Cidades com mais Restaurantes')
        fig = qtd_rest_cidade (df)
        st.plotly_chart(fig)

    st.markdown("""---""")
    with st.container():

        col1,col2 = st.columns(2, gap='large')

        with col1:
            # Bar plot - Top Cidades com nota acima de 4 
            st.markdown(f' #### Top {top_n} Cidades com Restaurantes com nota de availiação acima de 4')
            fig = top_cidade_nota_acima_4 (df)
            st.plotly_chart(fig , use_container_width=True)
        
        with col2:
            # Bar plot - Top cidades nota abaixo de 2,5
            st.markdown( f' ### Top {top_n} Cidades com Restaurantes com nota de avaliação abaixo de 2,5')
            fig = top_cidade_nota_abaixo_2meio (df)
            st.plotly_chart(fig , use_container_width=True)

with tab3: 
    st.title( ' Visão Restaurantes 🍽️')
    st.markdown("""---""")

    with st.container():
        # Bar plot - Top restaurantes com as melhores avaliações 
        st.markdown( f' ### Top {top_n} - Restaurantes com melhores nota de Avaliação')
        fig = top_rest_avaliacao (df)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""---""")
    with st.container():
        # Bar plot - Top Restaurantes com melhores pratos
        st.markdown(f' ### Top {top_n} - Restaurantes com o maior valor de prato para 2 pessoas')
        fig = top_rest_prato (df)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""---""")
    with st.container():

        col1, col2 = st.columns(2, gap='large')

        with col1:
            # Pie plot - Percentual de restaurantes que faz entregas
            st.markdown(f' ### Percentual de Restaurantes que fazem entregas online')
            fig = perc_rest_entregas (df)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # Pie plot - Percentual de restaurantes que faz reserva
            st.markdown (f' ### Percentural de Restaurantes que fazem Reservas de mesa')
            fig = perc_rest_reserva (df)
            st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.title('Visão Culinárias 🥗')
    st.markdown("""---""")

    with st.container():
        st.markdown( ' #### Melhores Restaurantes por tipo de Culinária')
        col1,col2,col3,col4 = st.columns(4, gap='large')

        with col1:
            st.markdown ( ' ##### Culinária Italiana ')
            linhas = df['unique_cuisines'] == 'Italian'
            colunas = ['restaurant_name' ,'aggregate_rating']
            df_aux= df.loc[linhas,colunas].groupby('restaurant_name').mean().sort_values('aggregate_rating',ascending=False).reset_index()
            culin = df_aux.iloc[0,0]
            media = df_aux.iloc[0,1]
            col1.metric(culin , media)

        with col2:
            st.markdown ( ' ##### Culinária Indiana')
            linhas = df['unique_cuisines'] == 'Indian'
            colunas = ['restaurant_name' ,'aggregate_rating']
            df_aux= df.loc[linhas,colunas].groupby('restaurant_name').mean().sort_values('aggregate_rating',ascending=False).reset_index()        
            culin = df_aux.iloc[0,0]
            media = df_aux.iloc[0,1]
            col2.metric(culin , media)

        with col3:
            st.markdown ( ' ##### Culinária Arabe    ')
            linhas = df['unique_cuisines'] == 'Arabian'
            colunas = ['restaurant_name' ,'aggregate_rating']
            df_aux= df.loc[linhas,colunas].groupby('restaurant_name').mean().sort_values('aggregate_rating',ascending=False).reset_index()        
            culin = df_aux.iloc[0,0]
            media = df_aux.iloc[0,1]
            col3.metric(culin , media)

        with col4:
            st.markdown ( ' ##### Culinária Japonesa ')
            linhas = df['unique_cuisines'] == 'Japanese'
            colunas = ['restaurant_name' ,'aggregate_rating']
            df_aux= df.loc[linhas,colunas].groupby('restaurant_name').mean().sort_values('aggregate_rating',ascending=False).reset_index()        
            culin = df_aux.iloc[0,0]
            media = df_aux.iloc[0,1]
            col4.metric(culin , media)

    st.markdown("""---""")
    with st.container():
        # Dataframe com top culinarias por notas 
        st.markdown(f' ### Top {top_n} - Culinárias com melhores avaliações na média.') 
        fig = top_culin_notas (df)
        st.dataframe(fig , use_container_width=True)

    st.markdown("""---""")
    with st.container():
        # Dataframe com Restaurantes que faz pedido online e entrega
        st.markdown(f' ### Top {top_n} - Culinárias com Restaurantes que aceitam pedidos online e fazem entregas.')
        fig = top_culin_pedido_entrega (df)
        st.dataframe(fig ,use_container_width=True)





