# PostAutomation Crew 🤖

![Robotic Crew](src/post_automation/img/robotic_crew.png)

Sistema de automação de currículos com múltiplos agentes de IA usando [CrewAI](https://crewai.com). Este projeto ajuda você a:

- 📎 Fazer upload do seu currículo (PDF)
- 🧠 Rodar análise automatizada com IA para validação do CV
- 🚀 Otimizar o currículo para vagas reais (com GitHub e portfólio, se disponíveis)
- 📄 Gerar um currículo novo (Markdown + PDF)
- ✉️ Criar uma cover letter sob demanda
- 🔐 Proteger acesso com login e senha (Streamlit)

---

## 🚀 Como rodar local

### 1. Clone o projeto e entre na pasta
```bash
git clone https://github.com/jhmartire/postautomation-crew.git
cd postautomation-crew
```

### 2. Crie seu ambiente virtual e ative
```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate  # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Crie um arquivo `.env`
```dotenv
OPENAI_API_KEY=sk-...
```

### 5. Rode com Streamlit
```bash
streamlit run src/post_automation/app.py
```

---

## 📦 Estrutura do Projeto
```
├── requirements.txt         # Dependências
├── .env                     # Chave da API (não sobe pro Git)
├── src/post_automation/
│   ├── app.py               # Página Streamlit
│   ├── run_project.py       # Executa os agentes
│   ├── main.py              # Execução local no terminal
│   ├── crew.py              # Lógica de montagem da crew
│   ├── tools/               # Ferramentas personalizadas
│   └── config/              # agents.yaml + tasks.yaml
```

---

## 🔐 Acesso Seguro
O sistema exige login com usuário e senha definidos diretamente no código do `app.py`. Ideal para evitar uso indevido quando se usa uma API paga como a da OpenAI.

---

## ☁️ Deploy no Streamlit Cloud
1. Suba este repositório para o seu GitHub ✅
2. Vá em [streamlit.io/cloud](https://streamlit.io/cloud)
3. Clique em **New App**
4. Conecte ao seu repositório e aponte para:  
   **`src/post_automation/app.py`**
5. Adicione a variável de ambiente `OPENAI_API_KEY`

---

## 📌 Requisitos
- Python >= 3.10 < 3.13
- Conta na OpenAI com chave ativa
- GitHub (para deploy)

---

## 🛡️ Aviso de Segurança
Nunca suba seu `.env` para o GitHub. O projeto já inclui `.gitignore` configurado para evitar isso.

---

Feito com ❤️ por [@jhmartire](https://github.com/jhmartire)
