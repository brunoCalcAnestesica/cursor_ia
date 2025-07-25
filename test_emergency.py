#!/usr/bin/env python3

from cursor_ia import CursorIA

def test_emergency():
    print("🧪 Testando comando de emergência...")
    
    try:
        assistant = CursorIA()
        print("✅ Assistente inicializado")
        
        print("🚨 Testando comando de emergência '!!!'")
        assistant.process_command('!!!')
        
        print("✅ Teste concluído!")
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")

if __name__ == "__main__":
    test_emergency() 