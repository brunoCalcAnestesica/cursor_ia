#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import time
import os
from datetime import datetime

# Importar as funcionalidades do Cursor IA
from cursor_ia import CursorIA

class CursorIAGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 Cursor IA - Assistente de Automação")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#2b2b2b')
        self.style.configure('TButton', background='#4CAF50', foreground='white', font=('Arial', 10, 'bold'))
        self.style.configure('TLabel', background='#2b2b2b', foreground='white', font=('Arial', 10))
        
        # Variáveis de controle
        self.assistant = None
        self.is_listening = False
        self.command_queue = queue.Queue()
        self.voice_thread = None
        
        # Criar interface
        self.create_widgets()
        
        # Inicializar assistente
        self.init_assistant()
        
        # Iniciar thread de processamento de comandos
        self.command_thread = threading.Thread(target=self.process_commands, daemon=True)
        self.command_thread.start()
    
    def create_widgets(self):
        """Criar widgets da interface"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Título
        title_label = tk.Label(main_frame, text="🤖 Cursor IA", 
                              font=('Arial', 20, 'bold'), 
                              bg='#2b2b2b', fg='#4CAF50')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame de entrada de comando
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        # Label para entrada de comando
        cmd_label = tk.Label(input_frame, text="Digite seu comando:", 
                            font=('Arial', 12, 'bold'), 
                            bg='#2b2b2b', fg='white')
        cmd_label.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
        
        # Campo de entrada de comando
        self.cmd_entry = tk.Entry(input_frame, font=('Arial', 12), 
                                 bg='#3c3c3c', fg='white', 
                                 insertbackground='white',
                                 relief='flat', bd=2)
        self.cmd_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.cmd_entry.bind('<Return>', self.execute_command)
        
        # Botão de executar comando
        self.execute_btn = tk.Button(input_frame, text="▶️ Executar", 
                                    font=('Arial', 12, 'bold'),
                                    bg='#4CAF50', fg='white',
                                    relief='flat', bd=0,
                                    command=self.execute_command)
        self.execute_btn.grid(row=1, column=1, padx=(0, 10))
        
        # Botão de voz
        self.voice_btn = tk.Button(input_frame, text="🎤 Ativar Voz", 
                                  font=('Arial', 12, 'bold'),
                                  bg='#2196F3', fg='white',
                                  relief='flat', bd=0,
                                  command=self.toggle_voice)
        self.voice_btn.grid(row=1, column=2)
        
        # Frame de log
        log_frame = ttk.Frame(main_frame)
        log_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Label do log
        log_label = tk.Label(log_frame, text="Log de Atividades:", 
                            font=('Arial', 12, 'bold'), 
                            bg='#2b2b2b', fg='white')
        log_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Área de log
        self.log_area = scrolledtext.ScrolledText(log_frame, 
                                                 font=('Consolas', 10),
                                                 bg='#1e1e1e', fg='#ffffff',
                                                 insertbackground='white',
                                                 relief='flat', bd=1)
        self.log_area.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame de controles
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(20, 0))
        
        # Botões de controle
        self.screenshot_btn = tk.Button(control_frame, text="📸 Screenshot", 
                                       font=('Arial', 10, 'bold'),
                                       bg='#FF9800', fg='white',
                                       relief='flat', bd=0,
                                       command=self.take_screenshot)
        self.screenshot_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.position_btn = tk.Button(control_frame, text="📍 Posição Mouse", 
                                     font=('Arial', 10, 'bold'),
                                     bg='#9C27B0', fg='white',
                                     relief='flat', bd=0,
                                     command=self.get_mouse_position)
        self.position_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = tk.Button(control_frame, text="🗑️ Limpar Log", 
                                  font=('Arial', 10, 'bold'),
                                  bg='#F44336', fg='white',
                                  relief='flat', bd=0,
                                  command=self.clear_log)
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = tk.Button(control_frame, text="⏹️ Parar Assistente", 
                                 font=('Arial', 10, 'bold'),
                                 bg='#607D8B', fg='white',
                                 relief='flat', bd=0,
                                 command=self.stop_assistant)
        self.stop_btn.pack(side=tk.RIGHT)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Status: Pronto")
        status_bar = tk.Label(main_frame, textvariable=self.status_var,
                             font=('Arial', 9), 
                             bg='#1e1e1e', fg='#4CAF50',
                             relief='sunken', bd=1)
        status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Adicionar comandos de exemplo
        self.add_example_commands()
    
    def add_example_commands(self):
        """Adicionar comandos de exemplo ao log"""
        examples = [
            "Comandos de exemplo:",
            "• mover para 500,300 - Move o mouse para coordenadas",
            "• clicar - Clique esquerdo na posição atual",
            "• clicar direito - Clique direito na posição atual",
            "• duplo clique - Duplo clique na posição atual",
            "• digitar olá mundo - Digita o texto especificado",
            "• pressionar enter - Pressiona a tecla especificada",
            "• tirar screenshot - Captura a tela",
            "• rolar para baixo - Rola a página para baixo",
            "• rolar para cima - Rola a página para cima",
            "• arrastar para 100,200 - Arrasta o mouse para coordenadas",
            "",
            "🚨 Comando de Emergência:",
            "• !!! - Fecha o assistente imediatamente",
            "",
            "Comandos inteligentes (com IA):",
            "• abrir o navegador",
            "• ir para o canto superior direito",
            "• selecionar tudo",
            "• copiar",
            "• colar",
            ""
        ]
        
        for example in examples:
            self.log_message(example, "info")
    
    def init_assistant(self):
        """Inicializar o assistente"""
        try:
            self.assistant = CursorIA()
            self.log_message("✅ Assistente inicializado com sucesso!", "success")
            self.status_var.set("Status: Assistente ativo")
        except Exception as e:
            self.log_message(f"❌ Erro ao inicializar assistente: {e}", "error")
            self.status_var.set("Status: Erro na inicialização")
    
    def log_message(self, message, level="info"):
        """Adicionar mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Cores para diferentes níveis
        colors = {
            "info": "#ffffff",
            "success": "#4CAF50",
            "error": "#F44336",
            "warning": "#FF9800",
            "voice": "#2196F3"
        }
        
        color = colors.get(level, "#ffffff")
        
        # Adicionar ao log
        self.log_area.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_area.see(tk.END)
        
        # Marcar com cor
        start = f"{self.log_area.index('end-2c').split('.')[0]}.0"
        end = f"{self.log_area.index('end-1c').split('.')[0]}.end"
        
        # Aplicar cor (simples, sem tags complexas)
        if level != "info":
            self.log_area.tag_add(level, start, end)
            self.log_area.tag_config(level, foreground=color)
    
    def execute_command(self, event=None):
        """Executar comando digitado"""
        command = self.cmd_entry.get().strip()
        if not command:
            return
        
        # Comando de emergência
        if command == '!!!':
            self.log_message("🚨 COMANDO DE EMERGÊNCIA ATIVADO!", "error")
            self.log_message("🛑 Fechando assistente...", "warning")
            self.root.after(1000, self.root.destroy)  # Fechar após 1 segundo
            return
        
        self.log_message(f"🎯 Executando: {command}", "info")
        self.cmd_entry.delete(0, tk.END)
        
        # Adicionar comando à fila
        self.command_queue.put(command)
    
    def process_commands(self):
        """Processar comandos da fila"""
        while True:
            try:
                command = self.command_queue.get(timeout=0.1)
                if command and self.assistant:
                    # Verificar comando de emergência
                    if command == '!!!':
                        self.log_message("🚨 COMANDO DE EMERGÊNCIA ATIVADO!", "error")
                        self.log_message("🛑 Fechando assistente...", "warning")
                        self.root.after(1000, self.root.destroy)  # Fechar após 1 segundo
                        continue
                    
                    try:
                        self.assistant.process_command(command)
                        self.log_message(f"✅ Comando executado: {command}", "success")
                    except Exception as e:
                        self.log_message(f"❌ Erro ao executar comando: {e}", "error")
            except queue.Empty:
                continue
            except Exception as e:
                self.log_message(f"❌ Erro no processamento: {e}", "error")
    
    def toggle_voice(self):
        """Alternar ativação de voz"""
        if not self.is_listening:
            self.start_voice_listening()
        else:
            self.stop_voice_listening()
    
    def start_voice_listening(self):
        """Iniciar escuta de voz"""
        if not self.assistant:
            messagebox.showerror("Erro", "Assistente não inicializado")
            return
        
        self.is_listening = True
        self.voice_btn.config(text="🔴 Parar Voz", bg='#F44336')
        self.status_var.set("Status: Escutando comandos de voz...")
        self.log_message("🎤 Ativação de voz iniciada", "voice")
        
        # Iniciar thread de voz
        self.voice_thread = threading.Thread(target=self.voice_listening_loop, daemon=True)
        self.voice_thread.start()
    
    def stop_voice_listening(self):
        """Parar escuta de voz"""
        self.is_listening = False
        self.voice_btn.config(text="🎤 Ativar Voz", bg='#2196F3')
        self.status_var.set("Status: Assistente ativo")
        self.log_message("🔇 Ativação de voz parada", "voice")
    
    def voice_listening_loop(self):
        """Loop de escuta de voz"""
        while self.is_listening:
            try:
                command = self.assistant.listen()
                if command:
                    self.log_message(f"🎤 Voz detectada: {command}", "voice")
                    # Executar comando em thread separada
                    threading.Thread(target=self.execute_voice_command, args=(command,), daemon=True).start()
            except Exception as e:
                if self.is_listening:  # Só logar se ainda estiver escutando
                    self.log_message(f"❌ Erro na escuta de voz: {e}", "error")
    
    def execute_voice_command(self, command):
        """Executar comando de voz"""
        try:
            self.assistant.process_command(command)
            self.log_message(f"✅ Comando de voz executado: {command}", "success")
        except Exception as e:
            self.log_message(f"❌ Erro ao executar comando de voz: {e}", "error")
    
    def take_screenshot(self):
        """Tirar screenshot"""
        if self.assistant:
            try:
                filename = self.assistant.take_screenshot()
                self.log_message(f"📸 Screenshot salvo: {filename}", "success")
            except Exception as e:
                self.log_message(f"❌ Erro ao tirar screenshot: {e}", "error")
    
    def get_mouse_position(self):
        """Obter posição do mouse"""
        if self.assistant:
            try:
                pos = self.assistant.get_mouse_position()
                self.log_message(f"📍 Posição do mouse: {pos}", "info")
            except Exception as e:
                self.log_message(f"❌ Erro ao obter posição: {e}", "error")
    
    def clear_log(self):
        """Limpar área de log"""
        self.log_area.delete(1.0, tk.END)
        self.add_example_commands()
        self.log_message("🗑️ Log limpo", "info")
    
    def stop_assistant(self):
        """Parar assistente"""
        if self.assistant:
            self.assistant.running = False
            self.stop_voice_listening()
            self.log_message("⏹️ Assistente parado", "warning")
            self.status_var.set("Status: Assistente parado")
    
    def on_closing(self):
        """Ação ao fechar a janela"""
        if self.assistant:
            self.assistant.running = False
        self.root.destroy()

def main():
    """Função principal"""
    root = tk.Tk()
    app = CursorIAGUI(root)
    
    # Configurar ação de fechamento
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Centralizar janela
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Iniciar loop principal
    root.mainloop()

if __name__ == "__main__":
    main() 