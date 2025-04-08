import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
from PIL import Image
import io
import os

# Nome do banco
db_path = "equipamentos.db"

# Cria a tabela, se não existir
def criar_tabela():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipamento TEXT,
            data_hora TEXT,
            matricula INTEGER,
            nome TEXT,
            status TEXT,
            obs TEXT,
            imagem BLOB
        )
    """)
    conn.commit()
    conn.close()

# Salvar no banco
def salvar_dados(equipamento, data_hora, matricula, nome, status, obs, imagem):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO equipamentos (equipamento, data_hora, matricula, nome, status, obs, imagem)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (equipamento, data_hora, matricula, nome, status, obs, imagem))
    conn.commit()
    conn.close()

# Carregar os dados do banco
def carregar_dados():
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM equipamentos", conn)
    conn.close()
    return df

# Iniciar
criar_tabela()

# Streamlit UI
st.title("Cadastro de Equipamentos com Imagem (SQLite)")

equipamento = st.text_input("Equipamento")
matricula = st.number_input("Matrícula", step=1)
nome = st.text_input("Nome")
status = st.selectbox("Status", ["Boa", "Qeb", "Em Manutenção"])
obs = st.text_area("Observações")
imagem_file = st.file_uploader("Imagem do Equipamento", type=["jpg", "jpeg", "png"])

if st.button("Salvar"):
    if equipamento and nome:
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        imagem_bytes = imagem_file.read() if imagem_file else None
        salvar_dados(equipamento, data_hora, matricula, nome, status, obs, imagem_bytes)
        st.success("Dados salvos com sucesso!")
        st.rerun()()
    else:
        st.warning("Preencha pelo menos o nome e o equipamento.")

# Mostrar os dados
st.subheader("Registros Salvos")
df = carregar_dados()
if not df.empty:
    for _, row in df.iterrows():
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(f"**Equipamento:** {row['equipamento']}")
            st.write(f"**Data/Hora:** {row['data_hora']}")
            st.write(f"**Matrícula:** {row['matricula']}")
            st.write(f"**Nome:** {row['nome']}")
            st.write(f"**Status:** {row['status']}")
            st.write(f"**Observações:** {row['obs']}")
        with col2:
            if row["imagem"]:
                img = Image.open(io.BytesIO(row["imagem"]))
                st.image(img, width=120, caption="Imagem")

