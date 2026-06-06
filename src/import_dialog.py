from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QCheckBox, QWidget,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from src.importer import ImportRow, ImportStatus
from src.theme import theme_manager


_LIGHT_COLORS = {
    ImportStatus.SAME:     {"bg": "#d4edda", "text": "#155724", "label": "Identisch"},
    ImportStatus.NEW:      {"bg": "#d1ecf1", "text": "#0c5460", "label": "Neu"},
    ImportStatus.CONFLICT: {"bg": "#fff3cd", "text": "#856404", "label": "Konflikt"},
}

_DARK_COLORS = {
    ImportStatus.SAME:     {"bg": "#1b3a2a", "text": "#75c98f", "label": "Identisch"},
    ImportStatus.NEW:      {"bg": "#0d2d38", "text": "#6bc9da", "label": "Neu"},
    ImportStatus.CONFLICT: {"bg": "#3a2e0d", "text": "#d4a017", "label": "Konflikt"},
}


class ImportPreviewDialog(QDialog):
    def __init__(self, rows: list[ImportRow], parent=None):
        super().__init__(parent)
        self.setWindowTitle("Import Vorschau")
        self.setMinimumSize(940, 540)
        self.resize(1020, 580)

        self._rows = rows
        self._checkboxes: list[QCheckBox] = []

        t = theme_manager.current
        colors = _DARK_COLORS if t.name == "dark" else _LIGHT_COLORS

        self.setStyleSheet(f"background: {t.content_bg}; color: {t.content_text};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 16)
        layout.setSpacing(10)

        # ── Title ─────────────────────────────────────────────────
        title = QLabel("Import Vorschau")
        title.setStyleSheet(
            f"color: {t.content_text}; font-size: 16px; font-weight: bold;"
        )
        layout.addWidget(title)

        # ── Summary ───────────────────────────────────────────────
        n_new      = sum(1 for r in rows if r.status == ImportStatus.NEW)
        n_same     = sum(1 for r in rows if r.status == ImportStatus.SAME)
        n_conflict = sum(1 for r in rows if r.status == ImportStatus.CONFLICT)

        summary_parts = []
        if n_new:
            c = colors[ImportStatus.NEW]
            summary_parts.append(
                f'<span style="color:{c["text"]};background:{c["bg"]};'
                f'padding:1px 6px;border-radius:4px;">'
                f'● {n_new} neu</span>'
            )
        if n_same:
            c = colors[ImportStatus.SAME]
            summary_parts.append(
                f'<span style="color:{c["text"]};background:{c["bg"]};'
                f'padding:1px 6px;border-radius:4px;">'
                f'● {n_same} identisch</span>'
            )
        if n_conflict:
            c = colors[ImportStatus.CONFLICT]
            summary_parts.append(
                f'<span style="color:{c["text"]};background:{c["bg"]};'
                f'padding:1px 6px;border-radius:4px;">'
                f'● {n_conflict} Konflikte</span>'
            )

        summary = QLabel("  ".join(summary_parts))
        summary.setTextFormat(Qt.RichText)
        summary.setStyleSheet("background: transparent;")
        layout.addWidget(summary)

        hint = QLabel(
            "Identisch = wird automatisch importiert  ·  "
            "Neu = standardmäßig ausgewählt  ·  "
            "Konflikt = bitte manuell bestätigen"
        )
        hint.setStyleSheet(f"color: {t.version_text}; font-size: 11px;")
        layout.addWidget(hint)

        # ── Table ─────────────────────────────────────────────────
        table = QTableWidget(len(rows), 6)
        table.setHorizontalHeaderLabels(
            ["", "Datum", "Ort / Route", "km", "Status", "Aktuell (bei Konflikt)"]
        )
        hh = table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.Fixed)
        table.setColumnWidth(0, 52)
        hh.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(2, QHeaderView.Interactive)
        table.setColumnWidth(2, 200)
        hh.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(5, QHeaderView.Stretch)
        table.setColumnWidth(5, 320)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(False)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setAlternatingRowColors(False)

        bold = QFont()
        bold.setBold(True)

        for i, row in enumerate(rows):
            c = colors[row.status]
            bg  = QColor(c["bg"])
            fg  = QColor(c["text"])

            # Checkbox (col 0) — centered in a wrapper widget
            cb = QCheckBox()
            cb.setChecked(row.status in (ImportStatus.NEW, ImportStatus.SAME))
            if row.status == ImportStatus.SAME:
                cb.setEnabled(False)
            self._checkboxes.append(cb)

            wrapper = QWidget()
            wrapper.setStyleSheet(f"background: {c['bg']};")
            wl = QHBoxLayout(wrapper)
            wl.setContentsMargins(0, 0, 0, 0)
            wl.setAlignment(Qt.AlignCenter)
            wl.addWidget(cb)
            table.setCellWidget(i, 0, wrapper)

            def _make_item(text: str, bg=bg, fg=fg) -> QTableWidgetItem:
                item = QTableWidgetItem(text)
                item.setBackground(bg)
                item.setForeground(fg)
                return item

            table.setItem(i, 1, _make_item(row.entry.date))
            table.setItem(i, 2, _make_item(row.entry.location))

            km_item = _make_item(row.entry.km)
            km_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(i, 3, km_item)

            status_item = _make_item(c["label"])
            status_item.setFont(bold)
            table.setItem(i, 4, status_item)

            if row.status == ImportStatus.CONFLICT and row.existing:
                curr_text = f"{row.existing.location}  ·  {row.existing.km} km"
                table.setItem(i, 5, _make_item(curr_text))
            else:
                table.setItem(i, 5, _make_item(""))

            table.setRowHeight(i, 28)

        table.setStyleSheet(f"""
            QTableWidget {{
                background: {t.content_bg}; color: {t.content_text};
                border: 1px solid {t.sidebar_border};
                border-radius: 8px; font-size: 13px; gridline-color: transparent;
            }}
            QTableWidget::item {{ padding: 2px 10px; border: none; }}
            QHeaderView::section {{
                background: {t.nav_hover}; color: {t.content_text};
                border: none; padding: 5px 8px;
                font-weight: bold; font-size: 12px;
            }}
            QScrollBar:vertical {{
                background: {t.nav_hover}; width: 8px;
                margin: 4px 2px; border-radius: 4px; border: none;
            }}
            QScrollBar::handle:vertical {{
                background: {t.nav_active_text}; border-radius: 4px; min-height: 24px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0; background: transparent;
            }}
        """)

        layout.addWidget(table)

        # ── Legend + Buttons ──────────────────────────────────────
        bottom = QHBoxLayout()

        select_all_btn = QPushButton("Alle auswählen")
        select_all_btn.setFixedHeight(30)
        select_all_btn.setStyleSheet(f"""
            QPushButton {{ background: transparent; color: {t.nav_active_text};
                border: 1px solid {t.nav_active_text}; border-radius: 6px;
                font-size: 12px; padding: 0 10px; }}
            QPushButton:hover {{ background: {t.nav_active_bg}; }}
        """)
        select_all_btn.clicked.connect(self._select_all_conflicts)

        bottom.addWidget(select_all_btn)
        bottom.addStretch()

        cancel_btn = QPushButton("Abbrechen")
        cancel_btn.setFixedHeight(34)
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{ background: transparent; color: {t.content_text};
                border: 1px solid {t.sidebar_border}; border-radius: 8px;
                font-size: 13px; padding: 0 14px; }}
            QPushButton:hover {{ background: {t.nav_hover}; }}
        """)

        ok_btn = QPushButton("Importieren")
        ok_btn.setFixedHeight(34)
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(self.accept)
        ok_btn.setStyleSheet(f"""
            QPushButton {{ background: {t.nav_active_text}; color: white;
                border: none; border-radius: 8px;
                font-size: 13px; font-weight: bold; padding: 0 14px; }}
            QPushButton:hover {{ background: {t.title_color}; }}
        """)

        bottom.addWidget(cancel_btn)
        bottom.addWidget(ok_btn)
        layout.addLayout(bottom)

    def _select_all_conflicts(self):
        for i, row in enumerate(self._rows):
            if row.status == ImportStatus.CONFLICT:
                self._checkboxes[i].setChecked(True)

    def selected_rows(self) -> list[ImportRow]:
        return [row for i, row in enumerate(self._rows) if self._checkboxes[i].isChecked()]
