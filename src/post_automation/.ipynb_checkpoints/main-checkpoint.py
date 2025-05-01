#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from crew import PostAutomation
from markdown2 import markdown
import pdfkit
import os

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# =======================
# Autenticação Simples
# =======================
AUTHORIZED_USER = "jhmartire"
AUTHORIZED_PASSWORD = "Fhqb9798"

print("🔐 Acesso Restrito - Login Obrigatório\n")
user = input("👤 Usuário: ").strip()
password = input("🔑 Senha: ").strip()

if user != AUTHORIZED_USER or password != AUTHORIZED_PASSWORD:
    print("❌ Acesso negado. Usuário ou senha incorretos.")
    sys.exit()

# =======================
# Função para gerar PDF
# =======================
def convert_markdown_to_pdf(input_md_path, output_pdf_path):
    if not os.path.exists(input_md_path):
        print(f"⚠️ Arquivo não encontrado: {input_md_path}")
        return
    with open(input_md_path, 'r', encoding='utf-8') as f:
        html = markdown(f.read())
        pdfkit.from_string(html, output_pdf_path)
        print(f"✅ PDF criado: {output_pdf_path}")

# =======================
# Execução principal
# =======================
def run():
    print("\n🚀 Bem-vindo ao PostAutomation Crew")
    print("Preencha os campos abaixo (pressione Enter para pular qualquer um):\n")

    job_posting = input("🔗 Link da vaga (LinkedIn, Indeed etc): ").strip()
    github_url = input("🐙 GitHub (opcional): ").strip()
    portfolio_url = input("🌐 Portfólio (opcional): ").strip()

    inputs = {
        'job_posting_url': job_posting if job_posting else "",
        'github_url': github_url if github_url else "",
        'personal_portfolio_url': portfolio_url if portfolio_url else ""
    }

    try:
        automation = PostAutomation()
        if not inputs["job_posting_url"] and not inputs["github_url"] and not inputs["personal_portfolio_url"]:
            print("🔍 Modo: Apenas Análise de CV")
            crew = automation.run_cv_only()
        else:
            print("🧠 Modo: Análise completa (CV + Vaga + GitHub/Portfólio)")
            crew = automation.crew()

        crew.kickoff(inputs=inputs)

        print("\n📄 Convertendo currículo gerado em PDF...")
        convert_markdown_to_pdf("tailored_resume.md", "tailored_resume.pdf")

        if os.path.exists("cover_letter.md"):
            print("✉️ Gerando cover letter em PDF...")
            convert_markdown_to_pdf("cover_letter.md", "cover_letter.pdf")
        else:
            print("ℹ️ Nenhuma cover letter foi gerada para esta vaga.")

    except Exception as e:
        raise Exception(f"❌ Erro durante a execução da crew: {e}")

# =======================
# Início do processo
# =======================
run()
