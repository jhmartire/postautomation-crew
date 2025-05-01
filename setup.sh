#!/bin/bash

echo "🔧 Iniciando setup automatizado do PostAutomation Crew..."

# 1. Criar ambiente virtual
if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv .venv
else
    echo "✅ Ambiente virtual já existe."
fi

# 2. Ativar ambiente virtual
echo "🚀 Ativando ambiente virtual..."
source .venv/bin/activate

# 3. Instalar dependências
echo "📦 Instalando dependências do requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Criar .env se não existir
if [ ! -f ".env" ]; then
    echo "🔐 Criando arquivo .env..."
    echo "OPENAI_API_KEY=sk-sua-chave-aqui" > .env
    echo "⚠️ Não esqueça de editar o .env com sua chave da OpenAI."
else
    echo "✅ Arquivo .env já existe."
fi

# 5. Rodar o app Streamlit
echo "🌐 Iniciando Streamlit..."
streamlit run src/post_automation/app.py
