from rich import print
from rich.text import Text
from rich.style import Style
from typing import List, Dict, Optional


class BarChart:
    def __init__(
        self,
        data: List[Dict[str, int]],
        width: int = 50,
        show_values: bool = True,
        show_percent: bool = True,
        color_scheme: Optional[List[str]] = None
    ):
        
        self.data = data
        self.width = width
        self.show_values = show_values
        self.show_percent = show_percent
        self.color_scheme = color_scheme or [
            "bright_red", "bright_green", "bright_blue",
            "bright_yellow", "bright_magenta", "bright_cyan",
            "bright_white",
        ]
        self.max_value = max(item['value'] for item in data)
        self.total_value = sum(item['value'] for item in data)

    def _get_bar(
        self,
        value: int,
        color: str,
        label: str,
        max_label_width: int
    ) -> Text:
        
        bar_length = int((value / self.max_value) * self.width)
        bar = "█" * bar_length
        text = Text()
        text.append(f"{label:<{max_label_width}} ", style="bold")
        text.append(bar, style=Style(color=color, bold=True))
        if self.show_values or self.show_percent:
            text.append(" ")
            if self.show_values:
                text.append(f"{value:,}", style="dim")
            if self.show_percent and self.total_value > 0:
                percent = (value / self.total_value) * 100
                text.append(f" ({percent:.1f}%)", style="dim")
        return text

    def render(self) -> None:
        
        max_label_width = max(len(item['name']) for item in self.data)
        for i, item in enumerate(self.data):
            color = self.color_scheme[i % len(self.color_scheme)]
            bar_text = self._get_bar(
                item['value'],
                color,
                item['name'],
                max_label_width
            )
            print(bar_text)