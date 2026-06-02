from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QScrollArea,
)
from PySide6.QtCore import Qt, Signal
from src.settings_data import load_routes, save_routes
from src.theme import theme_manager, Theme


class RouteRow(QWidget):
    deleted = Signal(str)

    def __init__(self, name: str):
        super().__init__()
        self._name = name
        self.setFixedHeight(38)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)

        self._label = QLabel(name)
        self._label.setStyleSheet("font-size: 13px;")
        layout.addWidget(self._label)
        layout.addStretch()

        self._del_btn = QPushButton("✕")
        self._del_btn.setFixedSize(24, 24)
        self._del_btn.setFlat(True)
        self._del_btn.setCursor(Qt.PointingHandCursor)
        self._del_btn.clicked.connect(lambda: self.deleted.emit(self._name))
        layout.addWidget(self._del_btn)

        self.apply_theme(theme_manager.current)

    def apply_theme(self, t: Theme):
        self.setStyleSheet(f"background: {t.content_bg}; border-bottom: 1px solid {t.sidebar_border};")
        self._label.setStyleSheet(f"background: transparent; color: {t.content_text}; font-size: 13px; border: none;")
        self._del_btn.setStyleSheet(f"""
            QPushButton {{ background: transparent; color: {t.version_text};
                border: none; border-radius: 12px; font-size: 11px; font-weight: bold; }}
            QPushButton:hover {{ background: #e06c75; color: white; }}
        """)


class SettingsView(QWidget):
    routes_changed = Signal()

    def __init__(self):
        super().__init__()
        self._rows: list[RouteRow] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(20)

        self._title = QLabel("Einstellungen")
        layout.addWidget(self._title)

        # ── Routen-Sektion ────────────────────────────────────────
        self._section = QFrame()
        self._section.setFrameShape(QFrame.NoFrame)
        sec_layout = QVBoxLayout(self._section)
        sec_layout.setContentsMargins(16, 14, 16, 14)
        sec_layout.setSpacing(10)

        self._sec_title = QLabel("Vordefinierte Routen / Orte")
        sec_layout.addWidget(self._sec_title)

        # Input row
        input_row = QHBoxLayout()
        self._input = QLineEdit()
        self._input.setPlaceholderText("Route oder Ort eingeben …")
        self._input.setFixedHeight(34)
        self._input.returnPressed.connect(self._add_route)
        input_row.addWidget(self._input)

        self._add_btn = QPushButton("+ Hinzufügen")
        self._add_btn.setFixedHeight(34)
        self._add_btn.setFixedWidth(120)
        self._add_btn.clicked.connect(self._add_route)
        input_row.addWidget(self._add_btn)
        sec_layout.addLayout(input_row)

        # Routes list
        self._list_box = QFrame()
        self._list_box.setFrameShape(QFrame.NoFrame)
        self._list_layout = QVBoxLayout(self._list_box)
        self._list_layout.setContentsMargins(0, 0, 0, 0)
        self._list_layout.setSpacing(0)
        sec_layout.addWidget(self._list_box)

        layout.addWidget(self._section)
        layout.addStretch()

        self._load()
        self.apply_theme(theme_manager.current)
        theme_manager.changed.connect(self.apply_theme)

    def _load(self):
        for row in self._rows:
            self._list_layout.removeWidget(row)
            row.setParent(None)
        self._rows.clear()

        for name in load_routes():
            self._add_row(name)

    def _add_row(self, name: str):
        row = RouteRow(name)
        row.deleted.connect(self._delete_route)
        self._list_layout.addWidget(row)
        self._rows.append(row)
        row.apply_theme(theme_manager.current)

    def _add_route(self):
        name = self._input.text().strip()
        if not name:
            return
        routes = load_routes()
        if name in routes:
            self._input.clear()
            return
        routes.append(name)
        save_routes(routes)
        self._add_row(name)
        self._input.clear()
        self.routes_changed.emit()

    def _delete_route(self, name: str):
        routes = [r for r in load_routes() if r != name]
        save_routes(routes)
        for row in self._rows:
            if row._name == name:
                self._list_layout.removeWidget(row)
                row.setParent(None)
                self._rows.remove(row)
                break
        self.routes_changed.emit()

    def apply_theme(self, t: Theme):
        self.setStyleSheet(f"background: {t.content_bg};")
        self._title.setStyleSheet(
            f"background: transparent; color: {t.content_text}; font-size: 22px; font-weight: bold;"
        )
        self._section.setStyleSheet(f"""
            QFrame {{ background: {t.nav_hover}; border: 1px solid {t.sidebar_border}; border-radius: 8px; }}
        """)
        self._sec_title.setStyleSheet(
            f"background: transparent; border: none; color: {t.content_text}; font-weight: bold; font-size: 14px;"
        )
        self._input.setStyleSheet(f"""
            QLineEdit {{ background: {t.content_bg}; color: {t.content_text};
                border: 1px solid {t.sidebar_border}; border-radius: 6px;
                padding: 4px 10px; font-size: 13px; }}
            QLineEdit:focus {{ border: 1px solid {t.nav_active_text}; }}
        """)
        self._add_btn.setStyleSheet(f"""
            QPushButton {{ background: {t.nav_active_text}; color: white; border: none;
                border-radius: 6px; font-size: 13px; font-weight: bold; }}
            QPushButton:hover {{ background: {t.title_color}; }}
        """)
        self._list_box.setStyleSheet("background: transparent; border: none;")
        for row in self._rows:
            row.apply_theme(t)
