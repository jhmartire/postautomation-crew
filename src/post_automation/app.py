import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
from src.post_automation.run_project import run_project

# Caminho para salvar o currículo enviado
RESUME_PATH = "src/post_automation/data/Joao_martire_resume.pdf"

# Configuração da página
st.set_page_config(page_title="PostAutomation Crew", layout="centered")

# --- Login simples ---
AUTHORIZED_USER = "jhmartire"
AUTHORIZED_PASSWORD = "Fhqb9798"

with st.sidebar:
    st.header("🔐 Login")
    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    login_button = st.button("Entrar")

# Validação de acesso
if not (user == AUTHORIZED_USER and password == AUTHORIZED_PASSWORD):
    st.warning("Acesso restrito. Insira credenciais válidas.")
    st.stop()

# Conteúdo principal
st.title("📄 PostAutomation Crew")
st.write("Otimize seu currículo com inteligência artificial e aplique para vagas com confiança!")

# Upload do currículo
uploaded_file = st.file_uploader("📎 Faça upload do seu currículo em PDF", type=["pdf"])

# Campos opcionais
job_url = st.text_input("🔗 Link da vaga (LinkedIn, Indeed, etc)", placeholder="https://...")
github = st.text_input("🐙 GitHub (opcional)", placeholder="https://github.com/seuperfil")
portfolio = st.text_input("🌐 Portfólio (opcional)", placeholder="https://meusite.com")

# Botão de execução
if st.button("🚀 Rodar análise"):
    if uploaded_file is None:
        st.error("⚠️ Por favor, envie um currículo em PDF antes de continuar.")
    else:
        # Salva o currículo enviado
        with open(RESUME_PATH, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Inputs tratados
        inputs = {
            "job_posting_url": job_url.strip(),
            "github_url": github.strip(),
            "personal_portfolio_url": portfolio.strip()
        }

        # Executa a lógica apropriada
        with st.spinner("⏳ Analisando seu currículo..."):
            try:
                run_project(inputs)
                st.success("✅ Análise concluída com sucesso!")
            except Exception as e:
                st.error(f"❌ Erro ao rodar o projeto: {e}")

        # Mostra os botões de download
        if os.path.exists("tailored_resume.pdf"):
            with open("tailored_resume.pdf", "rb") as f:
                st.download_button("📥 Baixar currículo otimizado", f, file_name="tailored_resume.pdf")

        if os.path.exists("cover_letter.pdf"):
            with open("cover_letter.pdf", "rb") as f:
                st.download_button("📥 Baixar cover letter", f, file_name="cover_letter.pdf")
        else:
            st.info("ℹ️ Nenhuma cover letter foi gerada para essa vaga.")
