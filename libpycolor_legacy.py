#!/usr/bin/env python3
# libpycolor_legacy.py (updated ycolor)
import sys
import time
import threading
import re
import subprocess

# --- ANSI colors + styles ---
class Colors:
    names = {
        "black": 0, "red": 1, "green": 2, "yellow": 3,
        "blue": 4, "magenta": 5, "cyan": 6, "white": 7,
        # extended
        "gold": 220, "chocolate": 94, "silver": 7, "pink": 200,
        "lime": 118, "turquoise": 80, "lavender": 189,
        "sky": 117, "salmon": 210
        # more can be added
    }
    for i in range(0, 256):
        if i not in names.values():
            names[f"color{i}"] = i

    styles = {"thin": 0, "bold": 1, "fancy": 3}

    @staticmethod
    def get_code(name):
        return Colors.names.get(name.lower(), 15)

    @staticmethod
    def get_style(style_name):
        return Colors.styles.get(style_name.lower(), 0)


# --- ycolor now prints directly ---
def ycolor(text: str):
    pattern = r"\[([a-zA-Z0-9]+):([a-zA-Z]+)\](.*?)\[/\1:\2\]"

    def repl(match):
        color_name = match.group(1)
        style_name = match.group(2)
        content = match.group(3)

        color_code = Colors.get_code(color_name)
        style_code = Colors.get_style(style_name)

        return f"\033[{style_code};38;5;{color_code}m{content}\033[0m"

    # Rainbow handling
    if "[rainbow]" in text and "[/rainbow]" in text:
        content = text.replace("[rainbow]", "").replace("[/rainbow]", "")
        rainbow_text(content)
        return  # rainbow prints inside rainbow_text

    # Normal text
    result = re.sub(pattern, repl, text)
    sys.stdout.write(result + "\n")
    sys.stdout.flush()


# --- rainbow prints directly ---
def rainbow_text(content: str, speed=0.05):
    rainbow_palette = [196, 202, 220, 46, 51, 21, 201, 208, 118, 129, 93]
    for i, char in enumerate(content):
        color_code = rainbow_palette[i % len(rainbow_palette)]
        sys.stdout.write(f"\033[1;38;5;{color_code}m{char}\033[0m")
        sys.stdout.flush()
        time.sleep(speed)
    print()


# --- ypre remains same ---
class ypre:
    symbols = {
        1: [".", "..", "...", "..", "."],
        2: ["|", "/", "-", "\\", "|", "/", "-", "\\"],
        3: ["*", "**", "***", "**", "*"],
        4: ["•", "••", "•••", "••", "•"],
        5: [" ", "▁", "▃", "▄", "▅", "▆", "▇", "█", "▇", "▆", "▅", "▄", "▃", "▁", " "]
    }

    @staticmethod
    def load(text, launch=None, sym=1, color="green:thin", interval=0.3):
        frames = ypre.symbols.get(sym, [".", "..", "..."])
        
        def run_command():
            if launch:
                subprocess.run(launch, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        thread = threading.Thread(target=run_command)
        thread.start()

        try:
            while thread.is_alive():
                for frame in frames:
                    output = f"{text}{frame}"
                    colored_output = re.sub(
                        r"\[([a-zA-Z0-9]+):([a-zA-Z]+)\](.*?)\[/\1:\2\]",
                        lambda m: f"\033[{Colors.get_style(m.group(2))};38;5;{Colors.get_code(m.group(1))}m{m.group(3)}\033[0m",
                        f"[{color}]{output}[/{color}]"
                    )
                    sys.stdout.write(f"\r{colored_output}")
                    sys.stdout.flush()
                    time.sleep(interval)
        except KeyboardInterrupt:
            pass
        finally:
            sys.stdout.write("\r" + " " * (len(text) + 20) + "\r")
            final_text = f"\033[3;38;5;{Colors.get_code('green')}m{text} Done\033[0m"
            print(final_text)
            thread.join()
