# libpycolor.py

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


# ---------------------------
# xcolor: colored text printer
# ---------------------------
class XColor:
    COLORS = {
        "green": "green",
        "yellow": "yellow",
        "red": "red",
        "chocolate": "sandy_brown",
        "pink": "pink1",
        "magenta": "magenta",
        "blue": "blue",
        "orange": "orange1",
        "purple": "purple",
        "cyan": "cyan",
        "gold": "gold1",
        "silver": "grey93",
        "white": "white",
        "black": "black",
    }

    @staticmethod
    def xcolor(text: str):
        """
        Prints text with [color]...[/color] tags.
        Example: xcolor("[red]Hello[/red] World")
        """
        styled = Text()
        while text:
            start = text.find("[")
            if start == -1:
                styled.append(text)
                break
            end = text.find("]", start)
            if end == -1:
                styled.append(text)
                break
            styled.append(text[:start])
            tag = text[start + 1 : end].lower()
            close_tag = f"[/{tag}]"
            text = text[end + 1 :]
            close_pos = text.lower().find(close_tag)
            if close_pos == -1:
                # no closing tag, treat literally
                styled.append(f"[{tag}]{text}")
                break
            inner_text = text[:close_pos]
            color = XColor.COLORS.get(tag, "white")
            styled.append(inner_text, style=color)
            text = text[close_pos + len(close_tag) :]
        console.print(styled)


xcolor = XColor.xcolor


# ---------------------------
# cages.box: unicode box with colored border
# ---------------------------
class CageBox:
    class Box:
        def __init__(self, title="", text="", border_color="white/white"):
            self.title = title
            self.text = text
            self.border_color = border_color
            self.__validate_border_color()

        def __validate_border_color(self):
            parts = self.border_color.split("/")
            if len(parts) != 2:
                raise ValueError(f"Invalid border.color: {self.border_color}")
            if parts[0].lower() != parts[1].lower():
                raise ValueError(
                    "Border color invalid: both sides must match (e.g., red/red)"
                )
            # Check if color exists
            if parts[0].lower() not in XColor.COLORS:
                raise ValueError(f"Unknown color: {parts[0]}")

        def show(self):
            color = XColor.COLORS[self.border_color.split("/")[0].lower()]
            panel = Panel(
                self.text,
                title=self.title,
                border_style=color,
                expand=False,
            )
            console.print(panel)


cages = type("cages", (), {"box": CageBox.Box})
