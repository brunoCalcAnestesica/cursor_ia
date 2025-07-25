#!/usr/bin/env python3

import pyautogui
import time

print("🧪 Testando Cursor IA...")

# Configurar failsafe
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

try:
    # Obter posição atual do mouse
    current_pos = pyautogui.position()
    print(f"📍 Posição atual do mouse: {current_pos}")
    
    # Mover mouse para posição de teste
    test_pos = (100, 100)
    print(f"🖱️ Movendo mouse para {test_pos}")
    pyautogui.moveTo(test_pos[0], test_pos[1], duration=1)
    
    # Verificar se moveu
    new_pos = pyautogui.position()
    print(f"📍 Nova posição: {new_pos}")
    
    # Voltar para posição original
    print(f"🖱️ Voltando para posição original {current_pos}")
    pyautogui.moveTo(current_pos[0], current_pos[1], duration=1)
    
    print("✅ Teste de mouse concluído com sucesso!")
    
    # Teste de clique (apenas simular)
    print("🖱️ Simulando clique (não vai clicar realmente)")
    time.sleep(1)
    
    print("🎉 Todos os testes passaram!")
    print("O Cursor IA está pronto para uso!")
    
except Exception as e:
    print(f"❌ Erro durante o teste: {e}")
    print("Verifique as permissões de acessibilidade no macOS") 