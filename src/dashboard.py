from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QHBoxLayout,
)
from PySide6.QtCore import Qt
from src.models import load_data, month_label
from src.theme import theme_manager, Theme

MAX_VISIBLE = 4


class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        self._expanded = False
        self._all_errors: list[str] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(20)

        self._title = QLabel("Dashboard")
        layout.addWidget(self._title)

        # Error box
        self._error_box = QFrame()
        self._error_box.setFrameShape(QFrame.NoFrame)
        self._box_layout = QVBoxLayout(self._error_box)
        self._box_layout.setContentsMargins(16, 12, 16, 12)
        self._box_layout.setSpacing(6)

        # Header row
        header_row = QHBoxLayout()
        self._error_title = QLabel("⚠  Ungültige Fahrstrecken")
        header_row.addWidget(self._error_title)
        header_row.addStretch()
        self._toggle_btn = QPushButton()
        self._toggle_btn.setFlat(True)
        self._toggle_btn.setFixedSize(80, 24)
        self._toggle_btn.setCursor(Qt.PointingHandCursor)
        self._toggle_btn.clicked.connect(self._toggle)
        self._toggle_btn.setVisible(False)
        header_row.addWidget(self._toggle_btn)
        self._box_layout.addLayout(header_row)

        self._error_label = QLabel()
        self._error_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self._error_label.setWordWrap(True)
        self._box_layout.addWidget(self._error_label)

        layout.addWidget(self._error_box)
        layout.addStretch()

        self.apply_theme(theme_manager.current)
        theme_manager.changed.connect(self.apply_theme)

    def _toggle(self):
        self._expanded = not self._expanded
        self._render_errors()

    def _render_errors(self):
        if not self._all_errors:
            self._error_label.setText("Keine Fehler gefunden.")
            self._toggle_btn.setVisible(False)
            return

        has_more = len(self._all_errors) > MAX_VISIBLE
        self._toggle_btn.setVisible(has_more)

        if has_more:
            self._toggle_btn.setText("▲ Weniger" if self._expanded else f"▼ Alle ({len(self._all_errors)})")

        shown = self._all_errors if self._expanded else self._all_errors[:MAX_VISIBLE]
        self._error_label.setText("\n".join(f"  • {e}" for e in shown))

    def refresh(self):
        data = load_data()
        self._all_errors = []

        for month_key in sorted(data.keys()):
            for entry in data[month_key]:
                km = entry.km.strip() if entry.km else ""
                if km and not km.lstrip("-").isdigit():
                    self._all_errors.append(
                        f"{month_label(month_key)}  ·  {entry.date}  –  \"{km}\""
                    )

        self._expanded = False
        self._render_errors()
        self.apply_theme(theme_manager.current)

    def apply_theme(self, t: Theme):
        self.setStyleSheet(f"background: {t.content_bg};")
        self._title.setStyleSheet(
            f"background: transparent; color: {t.content_text}; font-size: 22px; font-weight: bold;"
        )

        has_real_errors = bool(self._all_errors)
        if has_real_errors:
            box_bg, box_border, text_col = "#fff3cd", "#f0ad4e", "#856404"
        else:
            box_bg, box_border, text_col = t.nav_hover, t.sidebar_border, t.content_text

        self._error_box.setStyleSheet(f"""
            QFrame {{
                background: {box_bg};
                border: 1px solid {box_border};
                border-radius: 8px;
            }}
        """)
        self._error_title.setStyleSheet(
            f"background: transparent; color: {text_col}; font-weight: bold; font-size: 14px;"
        )
        self._error_label.setStyleSheet(
            f"background: transparent; color: {text_col}; font-size: 13px;"
        )
        self._toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent; color: {text_col};
                border: 1px solid {box_border}; border-radius: 4px;
                font-size: 11px;
            }}
            QPushButton:hover {{ background: {box_border}; }}
        """)
