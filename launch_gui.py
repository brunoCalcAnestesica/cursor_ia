#!/usr/bin/env python3

"""
Script de lançamento para o Cursor IA GUI
"""

import sys
import os

def main():
    print("🤖 Iniciando Cursor IA GUI...")
    
    # Verificar se tkinter está disponível
    try:
        import tkinter
        print("✅ Tkinter disponível")
    except ImportError:
        print("❌ Tkinter não encontrado. Instalando...")
        os.system("pip3 install tk")
        try:
            import tkinter
            print("✅ Tkinter instalado com sucesso")
        except ImportError:
            print("❌ Erro ao instalar Tkinter")
            return
    
    # Verificar se o arquivo principal existe
    if not os.path.exists("cursor_ia_gui.py"):
        print("❌ Arquivo cursor_ia_gui.py não encontrado")
        return
    
    # Verificar se o arquivo cursor_ia.py existe
    if not os.path.exists("cursor_ia.py"):
        print("❌ Arquivo cursor_ia.py não encontrado")
        return
    
    print("🚀 Lançando interface gráfica...")
    
    # Importar e executar a GUI
    try:
        from cursor_ia_gui import main as gui_main
        gui_main()
    except Exception as e:
        print(f"❌ Erro ao lançar GUI: {e}")
        print("Tentando executar diretamente...")
        os.system("python3 cursor_ia_gui.py")

if __name__ == "__main__":
    main() 