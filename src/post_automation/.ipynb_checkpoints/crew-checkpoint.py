from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew
from dotenv import load_dotenv
from crewai_tools import (
    FileReadTool,
    ScrapeWebsiteTool,
    MDXSearchTool,
    SerperDevTool,
    PDFSearchTool
)
from src.post_automation.tools.custom_tool import SkillMatchTool, UKEnglishTranslatorTool, CoverLetterTool

load_dotenv()

# Ferramentas
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
read_resume = FileReadTool(file_path='src/post_automation/data/Joao_martire_resume.pdf')
semantic_search_resume = MDXSearchTool(mdx='src/post_automation/data/Joao_martire_resume.pdf')
pdf_rag = PDFSearchTool(pdf='src/post_automation/data/Joao_martire_resume.pdf')
skill_match_tool = SkillMatchTool()
translator_tool = UKEnglishTranslatorTool()
cover_letter_tool = CoverLetterTool()

@CrewBase
class PostAutomation():

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def cv_validator(self) -> Agent:
        return Agent(
            config=self.agents_config['cv_validator'],
            tools=[read_resume, semantic_search_resume, pdf_rag],
            verbose=True
        )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=[scrape_tool, search_tool],
            verbose=True
        )

    @agent
    def profiler(self) -> Agent:
        return Agent(
            config=self.agents_config['profiler'],
            tools=[scrape_tool, search_tool, read_resume, semantic_search_resume, pdf_rag],
            verbose=True
        )

    @agent
    def resumer_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['resumer_strategist'],
            tools=[scrape_tool, search_tool, read_resume, semantic_search_resume, pdf_rag],
            allow_delegation=True,
            verbose=True
        )

    @agent
    def github_auditor(self) -> Agent:
        return Agent(
            config=self.agents_config['github_auditor'],
            tools=[skill_match_tool],
            verbose=True
        )

    @agent
    def translator(self) -> Agent:
        return Agent(
            config=self.agents_config['translator'],
            tools=[translator_tool],
            verbose=True
        )

    @agent
    def cover_letter_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['cover_letter_writer'],
            tools=[cover_letter_tool],
            verbose=True
        )

    def run_cv_only(self) -> Crew:
        validate_cv_task = Task(
            description=self.tasks_config['validate_cv_task']['description'],
            expected_output=self.tasks_config['validate_cv_task']['expected_output'],
            agent=self.cv_validator()
        )

        return Crew(
            agents=[self.cv_validator()],
            tasks=[validate_cv_task],
            verbose=True,
            process=Process.sequential,
            manager_llm='gpt-4o-mini'
        )

    @crew
    def crew(self) -> Crew:

        validate_cv_task = Task(
            description=self.tasks_config['validate_cv_task']['description'],
            expected_output=self.tasks_config['validate_cv_task']['expected_output'],
            agent=self.cv_validator()
        )

        research_task = Task(
            description=self.tasks_config['research_task']['description'],
            expected_output=self.tasks_config['research_task']['expected_output'],
            agent=self.researcher(),
            async_execution=True
        )

        profile_task = Task(
            description=self.tasks_config['profile_task']['description'],
            expected_output=self.tasks_config['profile_task']['expected_output'],
            agent=self.profiler(),
            async_execution=True
        )

        resume_strategy_task = Task(
            description=self.tasks_config['resume_strategy_task']['description'],
            expected_output=self.tasks_config['resume_strategy_task']['expected_output'],
            output_file="tailored_resume.md",
            context=[validate_cv_task, research_task, profile_task],
            agent=self.resumer_strategist()
        )

        github_audit_task = Task(
            description=self.tasks_config['github_audit_task']['description'],
            expected_output=self.tasks_config['github_audit_task']['expected_output'],
            context=[research_task, profile_task],
            agent=self.github_auditor(),
            async_execution=True
        )

        translation_task = Task(
            description=self.tasks_config['translation_task']['description'],
            expected_output=self.tasks_config['translation_task']['expected_output'],
            context=[resume_strategy_task],
            agent=self.translator()
        )

        cover_letter_task = Task(
            description=self.tasks_config['cover_letter_task']['description'],
            expected_output=self.tasks_config['cover_letter_task']['expected_output'],
            context=[research_task, profile_task],
            agent=self.cover_letter_writer()
        )

        return Crew(
            agents=self.agents,
            tasks=[
                validate_cv_task,
                research_task,
                profile_task,
                resume_strategy_task,
                github_audit_task,
                translation_task,
                cover_letter_task
            ],
            verbose=True,
            process=Process.hierarchical,
            manager_llm='gpt-4o-mini'
        )
