import os
import streamlit as st
import pandas as pd
from src.visualization import plot_radar_chart, plot_single_app_radar

# Configurações iniciais da página do Streamlit
st.set_page_config(
    page_title="Análise de Satisfação de Apps", 
    page_icon="data/Logo light mode.png"
    layout="wide")

# Título e logotipo
st.image("data/Logo light mode.png", width=200)
st.title("Análise de Satisfação de Apps")
st.write("Essa aplicação permite analisar a satisfação de usuários para diferentes aplicativos, com base nas subcategorias e médias de rating dos reviews.")

st.subheader("Upload de Arquivo CSV")

# Componente de upload
uploaded_file = st.file_uploader("Faça o upload de um arquivo .csv", type=["csv"])
df = None

if uploaded_file is not None:
    # Define o caminho para salvar o arquivo
    file_path = os.path.join("data", uploaded_file.name)

    # Salva o arquivo na pasta "data"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"Arquivo salvo em: {file_path}")

    # Carrega o arquivo em um DataFrame
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")

if df is not None:
    # Exibir uma tabela com o DataFrame processado para o radar
    st.subheader("Dados Processados para o Gráfico Radar")
    st.write("Tabela mostrando as **médias de rating nas avaliações**, por assuntos.")
    df_radar = df.groupby(['appId', 'subcategory'], as_index=False).agg({'avg_score': 'mean'}).pivot_table(
        index='appId', columns='subcategory', values='avg_score').fillna(0)
    st.dataframe(df_radar)

    # Exibir o gráfico radar geral com o arquivo CSV carregado
    st.subheader("Gráfico Radar de Satisfação - Todos os Apps")
    plot_radar_chart(file_path)

    # Controle para exibir o gráfico de um único app
    st.subheader("Análise Detalhada de um App")
    app_id_input = st.text_input("Digite o appId para visualizar o radar específico")

    # Verifica se o appId foi inserido e plota o gráfico específico
    if app_id_input:
        if app_id_input in df["appId"].unique():
            plot_single_app_radar(app_id_input, file_path)
        else:
            st.error("O appId informado não foi encontrado no arquivo de dados.")
