import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide") #Mostra como pagina cheia
##título
st.title('Teste veículos')

##dados para o app
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data ## armazena os dados em cash
def load_data(nrows): # função para buscar os dados
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# cria mensagem de texto dizendo que os dados estao sendo carregados.
data_load_state = st.text('Carregando Dados...')
# limita para Carregar 10.000 linhas de dados no dataframe.
data = load_data(10000)
# cria mensagem de texto dizendo ao leitor de que os dados foram carregados com sucesso.
data_load_state.text("Sucesso! (usando st.cache_data)")


# st.subheader('Dados') # cria um subtitulo antes da lista de dados
# st.write(data) # mostra a lista de dados

# as tres linha abaixo, substituem as duas linhas acima, caso queira um checkbos para ver ou nao os dados iniciais
if st.checkbox('Show raw data'): #cria um checkbox
    st.subheader('Raw data') # cria um subtitulo antes da lista de dados
    st.write(data) # mostra a lista de dados

st.subheader('Number of pickups by hour') # cria uma novo subtitulo "Número de coletas por hora"

#Utilize o NumPy para gerar um histograma que detalhe os horários de coleta agrupados por hora
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

# Agora, vamos usar st.bar_chart()o método do Streamlit para desenhar esse histograma.
st.bar_chart(hist_values)

# novo subtitulo (este trecho mostra um mapa com os pontos de coleta)
# st.subheader('Map of all pickups') #titulo "Mapa de todos os pontos de coleta"
# st.map(data) # mostra um grafico de mapa usando os dados do dataframe

# Depois de desenhar o histograma acima, você determinou que o horário de pico para 
# embarques da Uber era às 17h. Vamos redesenhar o mapa para mostrar a concentração 
# de embarques às 17h.


# novo subtitulo (este trecho mostra um mapa com os pontos de coleta filtrados pel ohorrio de maior pico as 17 horas)
#hour_to_filter = 17  #variavel digitaga manualmente apos análise
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h ##gera um controle deslizante para escolher a hora
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter] #filtra os dados somente do horario 17 horas
st.subheader(f'Map of all pickups at {hour_to_filter}:00') #gera subtitulo usando a variavel como parte do nome
st.map(filtered_data) # mostra um grafico de mapa usando os dados do dataframe

#Para desenhar este mapa, usamos a st.map função integrada do Streamlit, mas se você quiser visualizar dados de mapas complexos, recomendamos que você dê uma olhada no st.pydeck_chart.

