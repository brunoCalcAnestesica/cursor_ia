# 🤖 Cursor IA - Assistente de Automação

Um assistente de IA que controla o mouse e teclado do seu computador através de comandos de voz.

## 🚀 Funcionalidades

- **Controle de Mouse**: Mover, clicar, arrastar, duplo clique
- **Controle de Teclado**: Digitar texto, pressionar teclas
- **Reconhecimento de Voz**: Comandos em português
- **Síntese de Voz**: Feedback auditivo
- **Screenshots**: Captura de tela automática
- **IA Integrada**: Interpretação inteligente de comandos complexos

## 📋 Pré-requisitos

- Python 3.8+
- Microfone funcionando
- Alto-falantes ou fones de ouvido
- Conexão com internet

## 🛠️ Instalação

1. **Instalar dependências**:
```bash
pip install -r requirements.txt
```

2. **Configurar API Key** (opcional):
Crie um arquivo `.env` na raiz do projeto:
```
OPENAI_API_KEY=sua_chave_aqui
```

## 🎯 Como Usar

### Executar o assistente:
```bash
python cursor_ia.py
```

### Comandos de Voz Disponíveis:

#### 🖱️ Controle de Mouse:
- **"mover para x,y"** - Move o mouse para coordenadas específicas
- **"clicar"** - Clique esquerdo na posição atual
- **"clicar direito"** - Clique direito na posição atual
- **"duplo clique"** - Duplo clique na posição atual
- **"arrastar para x,y"** - Arrasta o mouse para coordenadas
- **"posição do mouse"** - Mostra a posição atual do mouse

#### ⌨️ Controle de Teclado:
- **"digitar [texto]"** - Digita o texto especificado
- **"pressionar [tecla]"** - Pressiona uma tecla específica
  - Exemplos: enter, space, tab, escape, ctrl, alt, shift

#### 📸 Outros Comandos:
- **"tirar screenshot"** ou **"capturar tela"** - Tira screenshot
- **"rolar para baixo/cima"** - Rola a página
- **"parar"** ou **"sair"** - Para o assistente

### Comandos Inteligentes (IA):
O assistente também entende comandos naturais como:
- **"abrir o navegador"**
- **"ir para o canto superior direito"**
- **"selecionar tudo"**
- **"copiar"**
- **"colar"**

## 🔧 Configuração Avançada

### Ajustar Sensibilidade do Microfone:
```python
# No arquivo cursor_ia.py, linha ~50
self.recognizer.adjust_for_ambient_noise(source, duration=1)
```

### Alterar Velocidade da Voz:
```python
# No arquivo cursor_ia.py, linha ~35
self.engine.setProperty('rate', 150)  # Palavras por minuto
```

### Configurar Timeout de Escuta:
```python
# No arquivo cursor_ia.py, linha ~55
audio = self.recognizer.listen(source, timeout=5)  # 5 segundos
```

## 🛡️ Segurança

- **Failsafe**: Mova o mouse para o canto superior esquerdo para parar o assistente
- **Pausa**: O assistente pausa 0.1 segundos entre ações para evitar execução muito rápida
- **Controle**: Use Ctrl+C no terminal para parar o programa

## 📝 Exemplos de Uso

### Cenário 1: Navegação Web
1. "mover para 500,300" (move para área de busca)
2. "clicar"
3. "digitar google.com"
4. "pressionar enter"

### Cenário 2: Captura de Tela
1. "tirar screenshot"
2. "mover para 100,100"
3. "clicar direito"
4. "rolar para baixo"

### Cenário 3: Automação de Formulário
1. "mover para 200,400"
2. "clicar"
3. "digitar João Silva"
4. "pressionar tab"
5. "digitar joao@email.com"

## 🔍 Solução de Problemas

### Microfone não funciona:
- Verifique as permissões do sistema
- Teste com `python -c "import speech_recognition; print('OK')"`

### Erro de API OpenAI:
- Verifique se a chave API está correta
- Confirme se há créditos disponíveis na conta

### Mouse não responde:
- Verifique se o PyAutoGUI está instalado corretamente
- Teste com `python -c "import pyautogui; print(pyautogui.position())"`

## 📚 Dependências Principais

- **pyautogui**: Controle de mouse e teclado
- **speech_recognition**: Reconhecimento de voz
- **pyttsx3**: Síntese de voz
- **openai**: IA para interpretação de comandos
- **pynput**: Controle de baixo nível de mouse/teclado

## 🤝 Contribuição

Sinta-se à vontade para contribuir com melhorias:
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

---

**⚠️ Aviso**: Este assistente tem acesso total ao seu mouse e teclado. Use com responsabilidade e sempre teste em um ambiente seguro primeiro. 