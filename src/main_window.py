from PySide6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QHBoxLayout,
    QWidget, QMessageBox, QPushButton, QStackedWidget,
)
from PySide6.QtCore import Qt, QThread, Signal
from version import __version__
from src.updater import check_for_update
from src.theme import theme_manager, Theme
from src.entry_view import EntryView
from src.dashboard import DashboardView


NAV_ITEMS = [
    ("Dashboard",   "🏠"),
    ("Daten",       "📋"),
    ("Analyse",     "📊"),
    ("Einstellungen", "⚙️"),
]


class UpdateChecker(QThread):
    update_available = Signal(dict)

    def __init__(self, version: str):
        super().__init__()
        self._version = version

    def run(self):
        result = check_for_update(self._version)
        if result:
            self.update_available.emit(result)


class NavButton(QPushButton):
    def __init__(self, icon: str, label: str):
        super().__init__(f"  {icon}  {label}")
        self.setCheckable(True)
        self.setFixedHeight(44)

    def apply_theme(self, t: Theme):
        self.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding-left: 12px;
                border: none;
                border-radius: 6px;
                color: {t.nav_text};
                font-size: 14px;
                background: transparent;
            }}
            QPushButton:hover {{
                background: {t.nav_hover};
            }}
            QPushButton:checked {{
                background: {t.nav_active_bg};
                color: {t.nav_active_text};
                font-weight: bold;
            }}
        """)


class Sidebar(QWidget):
    page_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self.setFixedWidth(210)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 16, 8, 16)
        layout.setSpacing(4)

        self._title = QLabel("DDKI")
        self._title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 8px 12px 16px 12px;")
        layout.addWidget(self._title)

        self._nav_buttons: list[NavButton] = []
        for i, (label, icon) in enumerate(NAV_ITEMS):
            btn = NavButton(icon, label)
            btn.clicked.connect(lambda checked, idx=i: self._select(idx))
            layout.addWidget(btn)
            self._nav_buttons.append(btn)

        layout.addStretch()

        self._version_label = QLabel(f"v{__version__}")
        self._version_label.setStyleSheet("font-size: 11px; padding: 4px 12px;")
        layout.addWidget(self._version_label)

        self._toggle_btn = QPushButton()
        self._toggle_btn.setFixedHeight(36)
        self._toggle_btn.clicked.connect(theme_manager.toggle)
        layout.addWidget(self._toggle_btn)

        self._select(0)
        self.apply_theme(theme_manager.current)

    def _select(self, index: int):
        for i, btn in enumerate(self._nav_buttons):
            btn.setChecked(i == index)
        self.page_changed.emit(index)

    def apply_theme(self, t: Theme):
        self.setStyleSheet(f"""
            QWidget {{
                background: {t.sidebar_bg};
            }}
            QWidget#sidebar {{
                border-right: 1px solid {t.sidebar_border};
            }}
        """)
        self._title.setStyleSheet(f"background: {t.sidebar_bg}; color: {t.title_color}; font-size: 20px; font-weight: bold; padding: 8px 12px 16px 12px;")
        self._version_label.setStyleSheet(f"background: {t.sidebar_bg}; color: {t.version_text}; font-size: 11px; padding: 4px 12px;")
        self._toggle_btn.setText(f"{t.toggle_icon}  Dark Mode" if t.name == "light" else f"{t.toggle_icon}  Light Mode")
        self._toggle_btn.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding-left: 12px;
                border: none;
                border-radius: 6px;
                color: {t.nav_text};
                font-size: 13px;
                background: {t.sidebar_bg};
            }}
            QPushButton:hover {{ background: {t.nav_hover}; }}
        """)
        for btn in self._nav_buttons:
            btn.apply_theme(t)


class ContentArea(QStackedWidget):
    def __init__(self):
        super().__init__()

        self._dashboard = DashboardView()   # index 0 – Dashboard
        self._entry_view = EntryView()      # index 1 – Dateien
        self.addWidget(self._dashboard)
        self.addWidget(self._entry_view)

        self._placeholder_labels: list[QLabel] = []
        for label, _ in NAV_ITEMS[2:]:      # Analyse, Einstellungen
            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignCenter)
            self.addWidget(lbl)
            self._placeholder_labels.append(lbl)

        self._dashboard.refresh()
        self.apply_theme(theme_manager.current)

    def on_page_changed(self, index: int):
        self.setCurrentIndex(index)
        if index == 0:
            self._dashboard.refresh()

    def apply_theme(self, t: Theme):
        self.setStyleSheet(f"background: {t.content_bg};")
        for lbl in self._placeholder_labels:
            lbl.setStyleSheet(f"background: {t.content_bg}; color: {t.content_text}; font-size: 22px;")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"DDKI v{__version__}")
        self.setMinimumSize(900, 600)

        root = QWidget()
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self._sidebar = Sidebar()
        self._content = ContentArea()

        root_layout.addWidget(self._sidebar)
        root_layout.addWidget(self._content)

        self._root = root
        self._sidebar.page_changed.connect(self._content.on_page_changed)
        self.setCentralWidget(root)

        theme_manager.changed.connect(self._on_theme_change)
        self._apply_root_theme(theme_manager.current)

        self._check_updates()

    def _apply_root_theme(self, t: Theme):
        self.setStyleSheet(f"QMainWindow {{ background: {t.content_bg}; }}")
        self._root.setStyleSheet(f"background: {t.content_bg};")

    def _on_theme_change(self, t: Theme):
        self._apply_root_theme(t)
        self._sidebar.apply_theme(t)
        self._content.apply_theme(t)

    def _check_updates(self):
        self._updater = UpdateChecker(__version__)
        self._updater.update_available.connect(self._on_update_found)
        self._updater.start()

    def _on_update_found(self, info: dict):
        msg = QMessageBox(self)
        msg.setWindowTitle("Update verfügbar")
        msg.setText(f"Version {info['version']} ist verfügbar.")
        msg.setInformativeText("Jetzt herunterladen?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if msg.exec() == QMessageBox.Yes:
            import webbrowser
            webbrowser.open(info["url"])
