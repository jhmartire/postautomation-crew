from crew import PostAutomation
from markdown2 import markdown
import os
import pdfkit

def convert_markdown_to_pdf(input_md_path, output_pdf_path):
    if not os.path.exists(input_md_path):
        return
    with open(input_md_path, 'r', encoding='utf-8') as f:
        html = markdown(f.read())
        pdfkit.from_string(html, output_pdf_path)

def run_project(inputs: dict):
    automation = PostAutomation()
    
    # Se nenhum campo foi preenchido, executa apenas a validação de CV
    if not inputs.get("job_posting_url") and not inputs.get("github_url") and not inputs.get("personal_portfolio_url"):
        crew = automation.run_cv_only()
    else:
        crew = automation.crew()
    
    crew.kickoff(inputs=inputs)

    convert_markdown_to_pdf("tailored_resume.md", "tailored_resume.pdf")

    if os.path.exists("cover_letter.md"):
        convert_markdown_to_pdf("cover_letter.md", "cover_letter.pdf")

