#!/bin/bash

echo "🤖 Instalando Cursor IA..."

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale o Python 3.8+ primeiro."
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"

# Criar ambiente virtual (opcional)
read -p "Deseja criar um ambiente virtual? (y/n): " create_venv
if [[ $create_venv == "y" || $create_venv == "Y" ]]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Ambiente virtual ativado"
fi

# Instalar dependências
echo "📦 Instalando dependências..."
pip install -r requirements.txt

# Verificar instalação
echo "🔍 Verificando instalação..."
python3 -c "
import pyautogui
import speech_recognition
import pyttsx3
import openai
print('✅ Todas as dependências instaladas com sucesso!')
"

# Configurar permissões (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 Configurando permissões para macOS..."
    echo "⚠️  Você pode precisar conceder permissões de acessibilidade:"
    echo "   1. Vá em Preferências do Sistema > Segurança e Privacidade > Privacidade"
    echo "   2. Selecione 'Acessibilidade'"
    echo "   3. Adicione o Terminal ou seu editor de código"
fi

echo ""
echo "🎉 Instalação concluída!"
echo ""
echo "Para executar o assistente:"
if [[ $create_venv == "y" || $create_venv == "Y" ]]; then
    echo "source venv/bin/activate"
fi
echo "python3 cursor_ia.py"
echo ""
echo "📖 Consulte o README_CURSOR_IA.md para mais informações." 