from dataclasses import dataclass
from PySide6.QtCore import QObject, Signal
from src.settings_data import load_theme, save_theme


@dataclass(frozen=True)
class Theme:
    name: str
    sidebar_bg: str
    sidebar_border: str
    title_color: str
    nav_text: str
    nav_hover: str
    nav_active_bg: str
    nav_active_text: str
    content_bg: str
    content_text: str
    version_text: str
    toggle_icon: str


LIGHT = Theme(
    name="light",
    sidebar_bg="#f5f5f5",
    sidebar_border="#e0e0e0",
    title_color="#5c5fef",
    nav_text="#333333",
    nav_hover="#ebebeb",
    nav_active_bg="#e4e4fb",
    nav_active_text="#5c5fef",
    content_bg="#ffffff",
    content_text="#222222",
    version_text="#aaaaaa",
    toggle_icon="🌙",
)

DARK = Theme(
    name="dark",
    sidebar_bg="#1e1e2e",
    sidebar_border="#313244",
    title_color="#cba6f7",
    nav_text="#cdd6f4",
    nav_hover="#313244",
    nav_active_bg="#45475a",
    nav_active_text="#cba6f7",
    content_bg="#181825",
    content_text="#cdd6f4",
    version_text="#585b70",
    toggle_icon="☀️",
)


class ThemeManager(QObject):
    changed = Signal(object)

    def __init__(self):
        super().__init__()
        self._theme = DARK if load_theme() == "dark" else LIGHT

    @property
    def current(self) -> Theme:
        return self._theme

    def toggle(self):
        self._theme = DARK if self._theme == LIGHT else LIGHT
        save_theme(self._theme.name)
        self.changed.emit(self._theme)


theme_manager = ThemeManager()
