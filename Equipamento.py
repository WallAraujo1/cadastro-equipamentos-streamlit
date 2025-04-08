import streamlit as st
import pandas as pd
from datetime import datetime
import os
from PIL import Image

# Nome do arquivo Excel
excel_file = 'equipamentos.xlsx'
imagem_dir = 'imagens_equipamentos'

# Cria a pasta para imagens, se não existir
if not os.path.exists(imagem_dir):
    os.makedirs(imagem_dir)

# Função para salvar os dados no Excel
def salvar_dados(dados, arquivo):
    if os.path.exists(arquivo):
        df_existente = pd.read_excel(arquivo)
        df_novo = pd.concat([df_existente, dados], ignore_index=True)
    else:
        df_novo = dados
    df_novo.to_excel(arquivo, index=False)

# Interface do app
st.set_page_config(page_title="Cadastro de Equipamentos", layout="wide")

menu = st.sidebar.selectbox("Menu", ["📝 Cadastro", "🔍 Consulta"])

# --- ABA CADASTRO ---
if menu == "📝 Cadastro":
    st.title("Cadastro de Equipamentos")

    equipamento = st.text_input("Equipamento")
    matricula = st.number_input("Matrícula", step=1)
    nome = st.text_input("Nome")
    status = st.selectbox("Status", ["Boa", "Qeb", "Em Manutenção"])
    obs = st.text_area("Observações")
    imagem = st.file_uploader("Enviar imagem", type=["png", "jpg", "jpeg"])

    if st.button("Salvar"):
        if equipamento and nome:
            data_hora = datetime.now()

            caminho_imagem = ""
            if imagem:
                extensao = imagem.name.split(".")[-1]
                nome_imagem = f"{equipamento}_{matricula}_{int(datetime.timestamp(data_hora))}.{extensao}"
                caminho_imagem = os.path.join(imagem_dir, nome_imagem)
                with open(caminho_imagem, "wb") as f:
                    f.write(imagem.read())

            novo_registro = pd.DataFrame({
                "EQUIPAMENTO": [equipamento],
                "DATA/HORA": [data_hora],
                "MATRICULA": [matricula],
                "NOME": [nome],
                "STATUS": [status],
                "OBS": [obs],
                "IMAGEM": [caminho_imagem]
            })
            salvar_dados(novo_registro, excel_file)
            st.success("Dados salvos com sucesso!")
        else:
            st.warning("Preencha pelo menos o nome e o equipamento.")

# --- ABA CONSULTA ---
elif menu == "🔍 Consulta":
    st.title("Consulta de Equipamentos")

    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)

        st.subheader("Últimos 10 Registros")
        ultimos = df.tail(10)

        for index, row in ultimos.iterrows():
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"""
                        **Equipamento:** {row['EQUIPAMENTO']}  
                        **Data/Hora:** {row['DATA/HORA']}  
                        **Matrícula:** {row['MATRICULA']}  
                        **Nome:** {row['NOME']}  
                        **Status:** {row['STATUS']}  
                        **Observações:** {row['OBS']}
                    """)
                with col2:
                    if pd.notna(row.get("IMAGEM")) and os.path.exists(row["IMAGEM"]):
                        st.image(row["IMAGEM"], width=100)
                    else:
                        st.markdown("_Sem imagem_")

        st.subheader("Filtrar por matrícula")
        matricula_busca = st.text_input("Digite a matrícula para buscar")
        if matricula_busca:
            resultados = df[df["MATRICULA"].astype(str).str.contains(matricula_busca)]
            if not resultados.empty:
                for index, row in resultados.iterrows():
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"""
                                **Equipamento:** {row['EQUIPAMENTO']}  
                                **Data/Hora:** {row['DATA/HORA']}  
                                **Matrícula:** {row['MATRICULA']}  
                                **Nome:** {row['NOME']}  
                                **Status:** {row['STATUS']}  
                                **Observações:** {row['OBS']}
                            """)
                        with col2:
                            if pd.notna(row.get("IMAGEM")) and os.path.exists(row["IMAGEM"]):
                                st.image(row["IMAGEM"], width=100)
                            else:
                                st.markdown("_Sem imagem_")
            else:
                st.info("Nenhum resultado encontrado.")
    else:
        st.info("Nenhum dado cadastrado ainda.")
