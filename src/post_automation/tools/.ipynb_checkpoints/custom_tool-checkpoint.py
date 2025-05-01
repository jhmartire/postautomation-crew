from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

# -------------------------
# GitHub Skill Match Tool
# -------------------------

class GitHubMatchInput(BaseModel):
    github_text: str = Field(..., description="Conteúdo do GitHub do candidato")
    job_description: str = Field(..., description="Descrição da vaga")

class SkillMatchTool(BaseTool):
    name: str = "GitHub Skill Match Analyzer"
    description: str = (
        "Verifica se as skills exigidas na descrição da vaga aparecem nos projetos do GitHub do candidato."
    )
    args_schema: Type[BaseModel] = GitHubMatchInput

    def _run(self, github_text: str, job_description: str) -> str:
        skills = ["python", "machine learning", "sql", "power bi", "data analysis", "git", "clustering", "regression"]
        job_text = job_description.lower()
        github_text = github_text.lower()

        matched = [skill for skill in skills if skill in job_text and skill in github_text]
        missing = [skill for skill in skills if skill in job_text and skill not in github_text]

        result = f"""
✅ Skills encontradas: {', '.join(matched) if matched else 'Nenhuma'}
❌ Ausentes: {', '.join(missing) if missing else 'Nenhuma'}
Sugestão: inclua projetos no GitHub que mostrem as skills ausentes.
"""
        return result.strip()


# -------------------------
# UK English Translator Tool
# -------------------------

class TranslateToUKInput(BaseModel):
    text: str = Field(..., description="Texto a ser traduzido para inglês britânico")

class UKEnglishTranslatorTool(BaseTool):
    name: str = "UK English Translator"
    description: str = "Traduz texto para inglês britânico com tom formal e profissional."
    args_schema: Type[BaseModel] = TranslateToUKInput

    def _run(self, text: str) -> str:
        uk_text = text.replace("analyze", "analyse").replace("organize", "organise")
        return f"(UK English Version)\n{uk_text}"


# -------------------------
# Cover Letter Generator Tool
# -------------------------

class CoverLetterInput(BaseModel):
    candidate_profile: str = Field(..., description="Resumo profissional do candidato")
    job_description: str = Field(..., description="Descrição da vaga")

class CoverLetterTool(BaseTool):
    name: str = "Cover Letter Generator"
    description: str = "Gera uma cover letter personalizada se a vaga exigir."
    args_schema: Type[BaseModel] = CoverLetterInput

    def _run(self, candidate_profile: str, job_description: str) -> str:
        if "cover letter" in job_description.lower():
            return f"""
Dear Hiring Manager,

I am writing to express my interest in the position recently advertised. With experience in {candidate_profile}, I believe my skills align strongly with your job requirements.

Thank you for considering my application.

Best regards,  
Joao Martire
"""
        else:
            return "Cover letter not required for this job posting."


# -------------------------
# CV Validation Tool (NOVO)
# -------------------------

class CVValidationInput(BaseModel):
    cv_text: str = Field(..., description="Texto extraído do currículo (PDF ou Markdown)")

class CVValidationTool(BaseTool):
    name: str = "CV Validator"
    description: str = "Analisa se o currículo está bem estruturado e identifica seções ausentes ou desalinhadas com o mercado."
    args_schema: Type[BaseModel] = CVValidationInput

    def _run(self, cv_text: str) -> str:
        recommendations = []

        if "summary" not in cv_text.lower():
            recommendations.append("Adicionar uma seção de 'Professional Summary'.")
        if "education" not in cv_text.lower():
            recommendations.append("Adicionar a seção 'Education'.")
        if "experience" not in cv_text.lower():
            recommendations.append("Adicionar a seção 'Professional Experience'.")
        if "skills" not in cv_text.lower():
            recommendations.append("Incluir uma seção clara de 'Skills'.")
        if not recommendations:
            return "✅ CV appears complete and properly structured."
        return "⚠️ Melhorias sugeridas:\n- " + "\n- ".join(recommendations)
