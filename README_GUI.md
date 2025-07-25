# 🖥️ Cursor IA - Interface Gráfica

Interface gráfica moderna para o Cursor IA com caixa de texto para comandos e botão de ativação de voz.

## 🎯 Funcionalidades da Interface

### 📝 Caixa de Comando
- **Campo de texto** para digitar comandos
- **Botão "Executar"** para enviar comandos
- **Enter** para executar rapidamente
- **Histórico** de comandos executados

### 🎤 Controle de Voz
- **Botão "Ativar Voz"** para iniciar escuta
- **Botão "Parar Voz"** para desativar escuta
- **Indicador visual** de status de escuta
- **Log em tempo real** dos comandos de voz

### 📊 Área de Log
- **Log colorido** com timestamps
- **Diferentes níveis**: info, success, error, warning, voice
- **Auto-scroll** para acompanhar atividades
- **Botão "Limpar Log"** para resetar

### 🎮 Botões de Controle
- **📸 Screenshot** - Captura tela instantânea
- **📍 Posição Mouse** - Mostra coordenadas atuais
- **🗑️ Limpar Log** - Limpa área de log
- **⏹️ Parar Assistente** - Para todas as operações

### 📱 Interface Moderna
- **Tema escuro** profissional
- **Cores intuitivas** para diferentes ações
- **Layout responsivo** e organizado
- **Status bar** com informações em tempo real

## 🚀 Como Usar

### 1. Lançar a Interface
```bash
# Opção 1: Script de lançamento
python3 launch_gui.py

# Opção 2: Execução direta
python3 cursor_ia_gui.py
```

### 2. Usar Comandos de Texto
1. Digite o comando na caixa de texto
2. Pressione **Enter** ou clique em **"Executar"**
3. Veja o resultado no log

### 3. Usar Comandos de Voz
1. Clique em **"🎤 Ativar Voz"**
2. Fale o comando claramente
3. O comando será executado automaticamente
4. Clique em **"🔴 Parar Voz"** para desativar

## 📝 Comandos Disponíveis

### 🖱️ Controle de Mouse
```
mover para 500,300
clicar
clicar direito
duplo clique
arrastar para 100,200
```

### ⌨️ Controle de Teclado
```
digitar olá mundo
pressionar enter
pressionar ctrl+a
pressionar tab
```

### 📸 Outros Comandos
```
tirar screenshot
rolar para baixo
rolar para cima
posição do mouse
```

### 🚨 Comando de Emergência
```
!!! - Fecha o assistente imediatamente
```

### 🤖 Comandos Inteligentes (com IA)
```
abrir o navegador
ir para o canto superior direito
selecionar tudo
copiar
colar
```

## 🎨 Características da Interface

### 🎯 Design
- **Tema escuro** (#2b2b2b)
- **Cores semânticas**:
  - Verde (#4CAF50) - Sucesso/Ações
  - Azul (#2196F3) - Voz/Informação
  - Vermelho (#F44336) - Erro/Parar
  - Laranja (#FF9800) - Screenshot
  - Roxo (#9C27B0) - Posição

### 📱 Layout
- **800x600 pixels** - Tamanho padrão
- **Centralizado** na tela
- **Grid responsivo** - Adapta ao conteúdo
- **Scroll automático** no log

### ⚡ Performance
- **Threading** para não travar a interface
- **Queue** para comandos assíncronos
- **Timeout** para comandos de voz
- **Failsafe** para operações seguras

## 🔧 Configuração

### 📋 Pré-requisitos
```bash
# Instalar dependências
pip3 install -r requirements.txt

# Verificar tkinter (geralmente já vem com Python)
python3 -c "import tkinter; print('✅ Tkinter OK')"
```

### 🔑 API Key (Opcional)
```bash
# Criar arquivo .env
echo "OPENAI_API_KEY=sua_chave_aqui" > .env
```

### 🍎 Permissões macOS
1. **Acessibilidade**: Preferências > Segurança > Privacidade > Acessibilidade
2. **Microfone**: Preferências > Segurança > Privacidade > Microfone
3. **Adicionar Terminal** ou seu editor de código

## 🛠️ Solução de Problemas

### ❌ Interface não abre
```bash
# Verificar tkinter
python3 -c "import tkinter; print('OK')"

# Instalar tkinter se necessário
pip3 install tk
```

### ❌ Comandos não funcionam
```bash
# Testar mouse primeiro
python3 test_cursor.py

# Verificar permissões no macOS
# Preferências > Segurança > Privacidade > Acessibilidade
```

### ❌ Voz não funciona
```bash
# Verificar microfone
python3 -c "import speech_recognition; print('OK')"

# Verificar permissões de microfone
# Preferências > Segurança > Privacidade > Microfone
```

### ❌ IA não funciona
```bash
# Verificar API key
cat .env

# Testar sem IA (funciona normalmente)
# Apenas comandos básicos serão disponíveis
```

## 📊 Log de Atividades

A interface mostra logs em tempo real com:

- **Timestamp** - Hora exata da ação
- **Cores** - Diferentes para cada tipo de ação
- **Status** - Sucesso, erro, aviso, etc.
- **Comandos** - Texto exato executado

### 🎨 Cores do Log
- **Branco** - Informações gerais
- **Verde** - Comandos executados com sucesso
- **Vermelho** - Erros e problemas
- **Laranja** - Avisos e paradas
- **Azul** - Atividades de voz

## 🎮 Exemplos de Uso

### 📝 Automação de Formulário
1. Digite: `mover para 200,400`
2. Digite: `clicar`
3. Digite: `digitar João Silva`
4. Digite: `pressionar tab`
5. Digite: `digitar joao@email.com`

### 🌐 Navegação Web
1. Digite: `mover para 500,300`
2. Digite: `clicar`
3. Digite: `digitar google.com`
4. Digite: `pressionar enter`

### 🎤 Comando de Voz
1. Clique em **"🎤 Ativar Voz"**
2. Fale: *"mover para o centro da tela"*
3. Fale: *"clicar"*
4. Fale: *"digitar olá mundo"*

## 🔒 Segurança

- **Failsafe**: Mova mouse para canto superior esquerdo
- **Timeout**: Comandos de voz têm limite de tempo
- **Threading**: Interface não trava durante operações
- **Validação**: Comandos são verificados antes da execução
- **🚨 Comando de Emergência**: Digite `!!!` para fechar imediatamente

## 📱 Compatibilidade

- ✅ **macOS** - Testado e funcionando
- ✅ **Windows** - Deve funcionar
- ✅ **Linux** - Deve funcionar
- ✅ **Python 3.8+** - Recomendado

---

**🎉 Aproveite o Cursor IA com interface gráfica moderna e intuitiva!** 