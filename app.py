import streamlit as st
import sqlite3
from datetime import datetime
from PIL import Image
import io

# Conectar ou criar o banco de dados
conn = sqlite3.connect("equipamentos.db", check_same_thread=False)
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS registros (
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

# Função para salvar dados no banco
def salvar_dados(equipamento, data_hora, matricula, nome, status, obs, imagem_bytes):
    cursor.execute("""
        INSERT INTO registros (equipamento, data_hora, matricula, nome, status, obs, imagem)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (equipamento, data_hora, matricula, nome, status, obs, imagem_bytes))
    conn.commit()

# Função para exibir dados
def carregar_dados():
    cursor.execute("SELECT equipamento, data_hora, matricula, nome, status, obs, imagem FROM registros")
    return cursor.fetchall()

# Interface Streamlit
st.title("Cadastro de Equipamentos - Banco SQLite")

equipamento = st.text_input("Equipamento")
matricula = st.number_input("Matrícula", step=1)
nome = st.text_input("Nome")
status = st.selectbox("Status", ["Boa", "Qeb", "Em Manutenção"])
obs = st.text_area("Observações")
imagem = st.file_uploader("Importar imagem (opcional)", type=["jpg", "jpeg", "png"])

if st.button("Salvar"):
    if equipamento and nome:
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        imagem_bytes = imagem.read() if imagem else None
        salvar_dados(equipamento, data_hora, matricula, nome, status, obs, imagem_bytes)
        st.success("Dados salvos com sucesso!")
    else:
        st.warning("Preencha pelo menos o nome e o equipamento.")

# Exibir os dados salvos
st.subheader("Registros Salvos")
dados = carregar_dados()

for eqp, dt, mat, nome, status, obs, img in dados:
    cols = st.columns([2, 2, 2, 1])
    with cols[0]:
        st.markdown(f"**Equipamento:** {eqp}")
        st.markdown(f"**Nome:** {nome}")
        st.markdown(f"**Matrícula:** {mat}")
    with cols[1]:
        st.markdown(f"**Status:** {status}")
        st.markdown(f"**Data:** {dt}")
    with cols[2]:
        st.markdown(f"**Obs:** {obs}")
    with cols[3]:
        if img:
            st.image(Image.open(io.BytesIO(img)), use_container_width=True)
