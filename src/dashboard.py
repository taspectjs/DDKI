import calendar
from datetime import date

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QHBoxLayout, QScrollArea,
)
from PySide6.QtCore import Qt, Signal
from src.models import load_data, month_label, current_month_key
from src.theme import theme_manager, Theme

MAX_VISIBLE = 4
DAYS_DE = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]


class MissingDayRow(QWidget):
    def __init__(self, date_str: str, on_add, on_skip):
        super().__init__()
        self.setFixedHeight(34)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 0, 4, 0)
        layout.setSpacing(8)

        d = date(2000 + int(date_str[6:8]), int(date_str[3:5]), int(date_str[0:2]))
        day_name = DAYS_DE[d.weekday()]
        is_weekend = d.weekday() >= 5

        self._label = QLabel(f"{day_name}  {date_str}")
        self._label.setFixedWidth(130)
        layout.addWidget(self._label)
        layout.addStretch()

        self._add_btn = QPushButton("+ Eintragen")
        self._add_btn.setFixedHeight(24)
        self._add_btn.setFixedWidth(90)
        self._add_btn.setCursor(Qt.PointingHandCursor)
        self._add_btn.clicked.connect(lambda _: on_add())
        layout.addWidget(self._add_btn)

        self._skip_btn = QPushButton("Überspringen")
        self._skip_btn.setFixedHeight(24)
        self._skip_btn.setFixedWidth(100)
        self._skip_btn.setCursor(Qt.PointingHandCursor)
        self._skip_btn.clicked.connect(lambda _: on_skip())
        layout.addWidget(self._skip_btn)

        self._is_weekend = is_weekend
        self.apply_theme(theme_manager.current)

    def apply_theme(self, t: Theme):
        color = t.version_text if self._is_weekend else t.content_text
        self.setStyleSheet("background: transparent;")
        self._label.setStyleSheet(f"background: transparent; color: {color}; font-size: 13px;")
        self._add_btn.setStyleSheet(f"""
            QPushButton {{
                background: {t.nav_active_bg}; color: {t.nav_active_text};
                border: none; border-radius: 5px; font-size: 11px; font-weight: bold;
            }}
            QPushButton:hover {{ background: {t.nav_active_text}; color: white; }}
        """)
        self._skip_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent; color: {t.version_text};
                border: 1px solid {t.sidebar_border}; border-radius: 5px; font-size: 11px;
            }}
            QPushButton:hover {{ background: {t.sidebar_border}; }}
        """)


class DashboardView(QWidget):
    navigate_to_date = Signal(str, str)   # (month_key, date_str)

    def __init__(self):
        super().__init__()
        self._err_expanded = False
        self._all_errors: list[str] = []
        self._miss_expanded = False
        self._missing_entries: list[tuple[str, str]] = []   # (month_key, date_str)
        self._skipped: set[tuple[str, str]] = set()
        self._miss_rows: list = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)

        self._title = QLabel("Dashboard")
        layout.addWidget(self._title)

        # ── Fehlende Einträge ──────────────────────────────────────
        self._miss_box = QFrame()
        self._miss_box.setFrameShape(QFrame.NoFrame)
        miss_outer = QVBoxLayout(self._miss_box)
        miss_outer.setContentsMargins(16, 12, 16, 12)
        miss_outer.setSpacing(6)

        miss_header = QHBoxLayout()
        self._miss_title = QLabel()
        miss_header.addWidget(self._miss_title)
        miss_header.addStretch()
        self._miss_toggle = QPushButton()
        self._miss_toggle.setFlat(True)
        self._miss_toggle.setFixedSize(90, 22)
        self._miss_toggle.setCursor(Qt.PointingHandCursor)
        self._miss_toggle.setVisible(False)
        self._miss_toggle.clicked.connect(self._toggle_missing)
        miss_header.addWidget(self._miss_toggle)
        miss_outer.addLayout(miss_header)

        self._miss_rows_widget = QWidget()
        self._miss_rows_widget.setStyleSheet("background: transparent;")
        self._miss_rows_layout = QVBoxLayout(self._miss_rows_widget)
        self._miss_rows_layout.setContentsMargins(0, 0, 0, 0)
        self._miss_rows_layout.setSpacing(2)
        miss_outer.addWidget(self._miss_rows_widget)
        layout.addWidget(self._miss_box)

        # ── Fehler ────────────────────────────────────────────────
        self._error_box = QFrame()
        self._error_box.setFrameShape(QFrame.NoFrame)
        err_layout = QVBoxLayout(self._error_box)
        err_layout.setContentsMargins(16, 12, 16, 12)
        err_layout.setSpacing(6)

        err_header = QHBoxLayout()
        self._error_title = QLabel("⚠  Ungültige Fahrstrecken")
        err_header.addWidget(self._error_title)
        err_header.addStretch()
        self._err_toggle = QPushButton()
        self._err_toggle.setFlat(True)
        self._err_toggle.setFixedSize(80, 22)
        self._err_toggle.setCursor(Qt.PointingHandCursor)
        self._err_toggle.setVisible(False)
        self._err_toggle.clicked.connect(self._toggle_errors)
        err_header.addWidget(self._err_toggle)
        err_layout.addLayout(err_header)

        self._error_label = QLabel()
        self._error_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self._error_label.setWordWrap(True)
        err_layout.addWidget(self._error_label)
        layout.addWidget(self._error_box)

        layout.addStretch()

        self.apply_theme(theme_manager.current)
        theme_manager.changed.connect(self.apply_theme)

    # ── Missing ───────────────────────────────────────────────────
    def _toggle_missing(self):
        self._miss_expanded = not self._miss_expanded
        self._render_missing()

    def _render_missing(self):
        for row in self._miss_rows:
            self._miss_rows_layout.removeWidget(row)
            row.setParent(None)
        self._miss_rows.clear()

        visible = [e for e in self._missing_entries if e not in self._skipped]
        has_more = len(visible) > MAX_VISIBLE
        self._miss_toggle.setVisible(has_more)
        if has_more:
            self._miss_toggle.setText("▲ Weniger" if self._miss_expanded else f"▼ Alle ({len(visible)})")

        shown = visible if self._miss_expanded else visible[:MAX_VISIBLE]

        if not shown:
            lbl = QLabel("Alle Einträge vollständig ✓")
            lbl.setStyleSheet(f"background: transparent; color: {theme_manager.current.content_text}; font-size: 13px;")
            self._miss_rows_layout.addWidget(lbl)
            self._miss_rows.append(lbl)
        else:
            for (mk, date_str) in shown:
                row = MissingDayRow(
                    date_str,
                    on_add=lambda m=mk, ds=date_str: self._on_add(m, ds),
                    on_skip=lambda m=mk, ds=date_str: self._on_skip(m, ds),
                )
                self._miss_rows_layout.addWidget(row)
                self._miss_rows.append(row)

        self.apply_theme(theme_manager.current)

    def _on_add(self, month_key: str, date_str: str):
        self.navigate_to_date.emit(month_key, date_str)

    def _on_skip(self, month_key: str, date_str: str):
        self._skipped.add((month_key, date_str))
        self._render_missing()

    # ── Errors ────────────────────────────────────────────────────
    def _toggle_errors(self):
        self._err_expanded = not self._err_expanded
        self._render_errors()

    def _render_errors(self):
        has_more = len(self._all_errors) > MAX_VISIBLE
        self._err_toggle.setVisible(has_more)
        if has_more:
            self._err_toggle.setText("▲ Weniger" if self._err_expanded else f"▼ Alle ({len(self._all_errors)})")
        shown = self._all_errors if self._err_expanded else self._all_errors[:MAX_VISIBLE]
        self._error_label.setText(
            "\n".join(f"  • {e}" for e in shown) if shown else "Keine Fehler gefunden."
        )

    # ── Refresh ───────────────────────────────────────────────────
    def refresh(self):
        data = load_data()
        today = date.today()
        cur_key = current_month_key()

        def missing_for(mk: str) -> list[tuple[str, str]]:
            try:
                parts = mk.split(".")
                m, y = int(parts[0]), int(parts[1])
            except (IndexError, ValueError):
                return []
            filled = {e.date for e in data.get(mk, []) if e.location.strip()}
            result = []
            for day in range(1, calendar.monthrange(y, m)[1] + 1):
                d = date(y, m, day)
                if d > today:
                    break
                date_str = d.strftime("%d.%m.%y")
                if date_str not in filled:
                    result.append((mk, date_str))
            return result

        # 1. Aktueller Monat hat Vorrang
        current_missing = missing_for(cur_key) if cur_key in data else []

        if current_missing:
            self._missing_entries = current_missing
            self._miss_title.setText(
                f"📋  Fehlende Einträge – {month_label(cur_key)} ({len(current_missing)})"
            )
        else:
            # 2. Ältesten unvollständigen Vergangenheitsmonat suchen
            past_keys = sorted(k for k in data if k != cur_key)
            active_mk = None
            active_missing = []
            for mk in past_keys:
                m = missing_for(mk)
                if m:
                    active_mk = mk
                    active_missing = m
                    break

            self._missing_entries = active_missing
            if active_mk:
                self._miss_title.setText(
                    f"📋  Fehlende Einträge – {month_label(active_mk)} ({len(active_missing)})"
                )
            else:
                self._miss_title.setText("📋  Fehlende Einträge")

        self._miss_expanded = False
        self._render_missing()

        self._all_errors = []
        for mk in sorted(data.keys()):
            for entry in data[mk]:
                km = entry.km.strip() if entry.km else ""
                if km and not km.lstrip("-").isdigit():
                    self._all_errors.append(f"{month_label(mk)}  ·  {entry.date}  –  \"{km}\"")

        self._err_expanded = False
        self._render_errors()
        self.apply_theme(theme_manager.current)

    # ── Theme ─────────────────────────────────────────────────────
    def apply_theme(self, t: Theme):
        self.setStyleSheet(f"background: {t.content_bg};")
        self._title.setStyleSheet(
            f"background: transparent; color: {t.content_text}; font-size: 22px; font-weight: bold;"
        )

        # missing box – blue tint
        self._miss_box.setStyleSheet(f"""
            QFrame {{ background: {t.nav_hover}; border: 1px solid {t.sidebar_border}; border-radius: 8px; }}
        """)
        self._miss_title.setStyleSheet(
            f"background: transparent; color: {t.content_text}; font-weight: bold; font-size: 14px;"
        )
        self._miss_toggle.setStyleSheet(f"""
            QPushButton {{ background: transparent; color: {t.content_text};
                border: 1px solid {t.sidebar_border}; border-radius: 4px; font-size: 11px; }}
            QPushButton:hover {{ background: {t.sidebar_border}; }}
        """)
        for row in self._miss_rows:
            if hasattr(row, "apply_theme"):
                row.apply_theme(t)

        # error box – yellow
        has_errors = bool(self._all_errors)
        bb, bbd, tc = ("#fff3cd", "#f0ad4e", "#856404") if has_errors else (t.nav_hover, t.sidebar_border, t.content_text)
        self._error_box.setStyleSheet(f"""
            QFrame {{ background: {bb}; border: 1px solid {bbd}; border-radius: 8px; }}
        """)
        self._error_title.setStyleSheet(f"background: transparent; color: {tc}; font-weight: bold; font-size: 14px;")
        self._error_label.setStyleSheet(f"background: transparent; color: {tc}; font-size: 13px;")
        self._err_toggle.setStyleSheet(f"""
            QPushButton {{ background: transparent; color: {tc};
                border: 1px solid {bbd}; border-radius: 4px; font-size: 11px; }}
            QPushButton:hover {{ background: {bbd}; }}
        """)
