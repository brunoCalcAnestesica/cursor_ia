import pyautogui
import cv2
import numpy as np
import time
import json
import os
from datetime import datetime
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
import speech_recognition as sr
import pyttsx3
import openai
from dotenv import load_dotenv
import threading
import queue

# Carregar variáveis de ambiente
load_dotenv()

class CursorIA:
    def __init__(self):
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.running = False
        self.command_queue = queue.Queue()
        
        # Inicializar OpenAI client apenas se a API key estiver disponível
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            try:
                self.openai_client = openai.OpenAI(api_key=api_key)
                self.ai_enabled = True
            except Exception as e:
                print(f"⚠️ Erro ao inicializar OpenAI: {e}")
                self.openai_client = None
                self.ai_enabled = False
        else:
            self.openai_client = None
            self.ai_enabled = False
        
        # Configurar reconhecimento de voz
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Configurar síntese de voz (opcional)
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.voice_enabled = True
        except Exception as e:
            print(f"⚠️ Síntese de voz não disponível: {e}")
            self.engine = None
            self.voice_enabled = False
        
        # Configurar PyAutoGUI
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
        # Histórico de comandos
        self.command_history = []
        
        print("🤖 Cursor IA inicializado!")
        print("Comandos disponíveis:")
        print("- 'mover para x,y': Move o mouse para coordenadas específicas")
        print("- 'clicar': Clica na posição atual do mouse")
        print("- 'clicar direito': Clica com botão direito")
        print("- 'duplo clique': Faz duplo clique")
        print("- 'arrastar para x,y': Arrasta o mouse para coordenadas")
        print("- 'digitar texto': Digita o texto especificado")
        print("- 'pressionar tecla': Pressiona uma tecla específica")
        print("- 'tirar screenshot': Captura a tela")
        print("- 'encontrar imagem': Procura uma imagem na tela")
        print("- 'parar': Para o assistente")
        
    def speak(self, text):
        """Sintetiza voz para o texto fornecido"""
        print(f"🤖 IA: {text}")
        if self.voice_enabled and self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"⚠️ Erro na síntese de voz: {e}")
    
    def listen(self):
        """Escuta comandos de voz"""
        try:
            with self.microphone as source:
                print("🎤 Ouvindo...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5)
                
            command = self.recognizer.recognize_google(audio, language='pt-BR')
            print(f"🎤 Você disse: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("❌ Não entendi o comando")
            return None
        except sr.RequestError:
            print("❌ Erro no reconhecimento de voz")
            return None
    
    def move_mouse(self, x, y):
        """Move o mouse para coordenadas específicas"""
        try:
            self.mouse.position = (int(x), int(y))
            print(f"🖱️ Mouse movido para ({x}, {y})")
            return True
        except Exception as e:
            print(f"❌ Erro ao mover mouse: {e}")
            return False
    
    def click(self, button='left'):
        """Clica com o mouse"""
        try:
            if button == 'left':
                self.mouse.click(Button.left)
                print("🖱️ Clique esquerdo")
            elif button == 'right':
                self.mouse.click(Button.right)
                print("🖱️ Clique direito")
            return True
        except Exception as e:
            print(f"❌ Erro ao clicar: {e}")
            return False
    
    def double_click(self):
        """Faz duplo clique"""
        try:
            self.mouse.click(Button.left, 2)
            print("🖱️ Duplo clique")
            return True
        except Exception as e:
            print(f"❌ Erro no duplo clique: {e}")
            return False
    
    def drag(self, x, y):
        """Arrasta o mouse para coordenadas"""
        try:
            current_pos = self.mouse.position
            pyautogui.drag(int(x) - current_pos[0], int(y) - current_pos[1], duration=0.5)
            print(f"🖱️ Arrastado para ({x}, {y})")
            return True
        except Exception as e:
            print(f"❌ Erro ao arrastar: {e}")
            return False
    
    def type_text(self, text):
        """Digita texto"""
        try:
            self.keyboard.type(text)
            print(f"⌨️ Digitado: {text}")
            return True
        except Exception as e:
            print(f"❌ Erro ao digitar: {e}")
            return False
    
    def press_key(self, key_name):
        """Pressiona uma tecla específica"""
        try:
            key_map = {
                'enter': Key.enter,
                'space': Key.space,
                'tab': Key.tab,
                'escape': Key.esc,
                'backspace': Key.backspace,
                'delete': Key.delete,
                'ctrl': Key.ctrl,
                'alt': Key.alt,
                'shift': Key.shift
            }
            
            if key_name.lower() in key_map:
                self.keyboard.press(key_map[key_name.lower()])
                self.keyboard.release(key_map[key_name.lower()])
                print(f"⌨️ Tecla pressionada: {key_name}")
            else:
                self.keyboard.press(key_name)
                self.keyboard.release(key_name)
                print(f"⌨️ Tecla pressionada: {key_name}")
            return True
        except Exception as e:
            print(f"❌ Erro ao pressionar tecla: {e}")
            return False
    
    def take_screenshot(self, filename=None):
        """Tira screenshot da tela"""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            print(f"📸 Screenshot salvo como: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Erro ao tirar screenshot: {e}")
            return None
    
    def find_image(self, image_path, confidence=0.8):
        """Procura uma imagem na tela"""
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                center = pyautogui.center(location)
                print(f"🔍 Imagem encontrada em: {center}")
                return center
            else:
                print("🔍 Imagem não encontrada na tela")
                return None
        except Exception as e:
            print(f"❌ Erro ao procurar imagem: {e}")
            return None
    
    def get_mouse_position(self):
        """Retorna a posição atual do mouse"""
        pos = self.mouse.position
        print(f"🖱️ Posição atual do mouse: {pos}")
        return pos
    
    def scroll(self, direction='down', clicks=3):
        """Rola a página"""
        try:
            if direction == 'down':
                pyautogui.scroll(-clicks)
                print(f"📜 Rolado para baixo ({clicks} cliques)")
            elif direction == 'up':
                pyautogui.scroll(clicks)
                print(f"📜 Rolado para cima ({clicks} cliques)")
            return True
        except Exception as e:
            print(f"❌ Erro ao rolar: {e}")
            return False
    
    def process_command(self, command):
        """Processa comandos de voz/texto"""
        if not command:
            return
        
        # Adicionar ao histórico
        self.command_history.append({
            'command': command,
            'timestamp': datetime.now().isoformat()
        })
        
        # Comandos básicos
        if 'mover para' in command:
            try:
                # Extrair coordenadas do comando
                coords = command.split('mover para')[1].strip()
                if ',' in coords:
                    x, y = coords.split(',')
                    self.move_mouse(int(x.strip()), int(y.strip()))
                else:
                    print("❌ Formato inválido. Use: 'mover para x,y'")
            except:
                print("❌ Formato inválido. Use: 'mover para x,y'")
        
        elif 'clicar' in command:
            if 'direito' in command:
                self.click('right')
            else:
                self.click('left')
        
        elif 'duplo clique' in command:
            self.double_click()
        
        elif 'arrastar para' in command:
            try:
                coords = command.split('arrastar para')[1].strip()
                if ',' in coords:
                    x, y = coords.split(',')
                    self.drag(int(x.strip()), int(y.strip()))
                else:
                    print("❌ Formato inválido. Use: 'arrastar para x,y'")
            except:
                print("❌ Formato inválido. Use: 'arrastar para x,y'")
        
        elif 'digitar' in command:
            text = command.split('digitar')[1].strip()
            self.type_text(text)
        
        elif 'pressionar' in command:
            key = command.split('pressionar')[1].strip()
            self.press_key(key)
        
        elif 'screenshot' in command or 'capturar tela' in command:
            self.take_screenshot()
        
        elif 'posição' in command and 'mouse' in command:
            self.get_mouse_position()
        
        elif 'rolar' in command:
            if 'baixo' in command:
                self.scroll('down')
            elif 'cima' in command:
                self.scroll('up')
        
        elif 'parar' in command or 'sair' in command:
            self.running = False
            self.speak("Parando o assistente")
        
        elif command == '!!!':
            self.running = False
            self.speak("Comando de emergência ativado. Fechando assistente.")
            print("🚨 COMANDO DE EMERGÊNCIA ATIVADO!")
            print("🛑 Fechando assistente...")
        
        else:
            # Usar IA para interpretar comandos complexos
            self.interpret_with_ai(command)
    
    def interpret_with_ai(self, command):
        """Usa OpenAI para interpretar comandos complexos"""
        if not self.ai_enabled or not self.openai_client:
            print(f"ℹ️ IA não disponível. Comando não reconhecido: {command}")
            print("   Configure OPENAI_API_KEY para usar comandos inteligentes")
            return
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """Você é um assistente de automação de computador. 
                        Analise o comando do usuário e retorne uma ação JSON válida.
                        Ações disponíveis:
                        - move_mouse: {"action": "move_mouse", "x": int, "y": int}
                        - click: {"action": "click", "button": "left"|"right"}
                        - double_click: {"action": "double_click"}
                        - type_text: {"action": "type_text", "text": "string"}
                        - press_key: {"action": "press_key", "key": "string"}
                        - take_screenshot: {"action": "take_screenshot"}
                        - get_position: {"action": "get_position"}
                        - scroll: {"action": "scroll", "direction": "up"|"down", "clicks": int}
                        - none: {"action": "none", "message": "string"}
                        
                        Retorne apenas o JSON, sem texto adicional."""
                    },
                    {
                        "role": "user",
                        "content": f"Comando: {command}"
                    }
                ],
                max_tokens=100
            )
            
            try:
                action = json.loads(response.choices[0].message.content)
                self.execute_action(action)
            except json.JSONDecodeError:
                print("❌ Erro ao interpretar resposta da IA")
                
        except Exception as e:
            print(f"❌ Erro ao usar IA: {e}")
    
    def execute_action(self, action):
        """Executa ação retornada pela IA"""
        action_type = action.get('action')
        
        if action_type == 'move_mouse':
            self.move_mouse(action['x'], action['y'])
        elif action_type == 'click':
            self.click(action['button'])
        elif action_type == 'double_click':
            self.double_click()
        elif action_type == 'type_text':
            self.type_text(action['text'])
        elif action_type == 'press_key':
            self.press_key(action['key'])
        elif action_type == 'take_screenshot':
            self.take_screenshot()
        elif action_type == 'get_position':
            self.get_mouse_position()
        elif action_type == 'scroll':
            self.scroll(action['direction'], action.get('clicks', 3))
        elif action_type == 'none':
            print(f"ℹ️ {action.get('message', 'Comando não reconhecido')}")
    
    def run(self):
        """Executa o assistente"""
        self.running = True
        self.speak("Assistente ativado. Aguardando comandos.")
        
        while self.running:
            try:
                # Escutar comando de voz
                command = self.listen()
                if command:
                    self.process_command(command)
                
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\n🛑 Interrompido pelo usuário")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")
        
        self.speak("Assistente desativado")

if __name__ == "__main__":
    # Verificar se a API key está configurada
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  OPENAI_API_KEY não encontrada nas variáveis de ambiente")
        print("   Crie um arquivo .env com: OPENAI_API_KEY=sua_chave_aqui")
        print("   Ou configure a variável de ambiente OPENAI_API_KEY")
        print("   O assistente funcionará sem IA para comandos complexos")
    
    # Criar e executar o assistente
    assistant = CursorIA()
    assistant.run() 