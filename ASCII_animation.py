import time
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_startup_animation():
    # Nueva animación con emojis y estilo Hobbesiano
    frames = [
        """
        🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
        🌊   🐙 LEVIATÁN   🌊
        🌊   Hobbesiano   🌊
        🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
        """,
        """
        ⚓⚓⚓⚓⚓⚓⚓⚓⚓⚓⚓⚓
        ⚓  🦑 Navegando  ⚓
        ⚓  en abismos  ⚓
        ⚓⚓⚓⚓⚓⚓⚓⚓⚓⚓⚓⚓
        """,
        """
        🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
        🔥   ¡Despierta!  🔥
        🔥  el Leviatán   🔥
        🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
        """,
        """
        🐚🐚🐚🐚🐚🐚🐚🐚🐚🐚🐚🐚
        🐚   Conquista   🐚
        🐚  la penumbra  🐚
        🐚🐚🐚🐚🐚🐚🐚🐚🐚🐚🐚🐚
        """
    ]
    
    for _ in range(3):  # Animación repetida 3 veces
        for frame in frames:
            clear_console()
            print(frame)
            time.sleep(0.5)
