import calendar
from datetime import date
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QHeaderView, QAbstractItemView, QFrame,
    QDialog, QComboBox, QSpinBox, QDialogButtonBox,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont
from src.models import Entry, load_data, save_data, current_month_key, month_label
from src.theme import theme_manager, Theme


MONTH_NAMES = ["Januar", "Februar", "März", "April", "Mai", "Juni",
               "Juli", "August", "September", "Oktober", "November", "Dezember"]


class MonthPickerDialog(QDialog):
    def __init__(self, default_key: str, existing_keys: list[str], parent=None):
        super().__init__(parent)
        self.setWindowTitle("Monat hinzufügen")
        self.setFixedSize(280, 140)

        t = theme_manager.current
        self.setStyleSheet(f"background: {t.content_bg}; color: {t.content_text};")

        m, y = int(default_key.split(".")[0]), int(default_key.split(".")[1])

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        row = QHBoxLayout()

        self._month_box = QComboBox()
        for name in MONTH_NAMES:
            self._month_box.addItem(name)
        self._month_box.setCurrentIndex(m - 1)
        self._month_box.setFixedHeight(34)

        self._year_spin = QSpinBox()
        self._year_spin.setRange(2000, 2100)
        self._year_spin.setValue(y)
        self._year_spin.setFixedWidth(80)
        self._year_spin.setFixedHeight(34)

        row.addWidget(self._month_box)
        row.addWidget(self._year_spin)
        layout.addLayout(row)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        field = f"background: {t.content_bg}; color: {t.content_text}; border: 1px solid {t.sidebar_border}; border-radius: 6px; padding: 4px 8px; font-size: 13px;"
        self._month_box.setStyleSheet(field)
        self._year_spin.setStyleSheet(field)
        buttons.setStyleSheet(f"""
            QPushButton {{
                background: {t.nav_active_text}; color: white; border: none;
                border-radius: 6px; padding: 6px 16px; font-size: 13px;
            }}
            QPushButton[text="Cancel"], QPushButton[text="Abbrechen"] {{
                background: transparent; color: {t.content_text};
                border: 1px solid {t.sidebar_border};
            }}
        """)

    def result_key(self) -> str:
        m = self._month_box.currentIndex() + 1
        y = self._year_spin.value()
        return f"{m:02d}.{y}"


class MonthList(QWidget):
    month_selected = Signal(str)
    month_delete_requested = Signal(str)

    def __init__(self):
        super().__init__()
        self._rows: dict[str, QWidget] = {}
        self._buttons: dict[str, QPushButton] = {}
        self._selected: str | None = None

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(8, 8, 8, 8)
        self._layout.setSpacing(4)

        self._header = QLabel("Monate")
        self._layout.addWidget(self._header)

        self._layout.addStretch()

        self._add_btn = QPushButton("+ Monat")
        self._add_btn.setFixedHeight(34)
        self._layout.addWidget(self._add_btn)

        self.apply_theme(theme_manager.current)

    def populate(self, keys: list[str], select_key: str | None = None):
        for row in self._rows.values():
            self._layout.removeWidget(row)
            row.setParent(None)
        self._rows.clear()
        self._buttons.clear()

        insert_at = 1
        for key in keys:
            row = QWidget()
            row.setFixedHeight(36)
            row.setAttribute(Qt.WA_StyledBackground, False)
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 2, 4, 2)
            row_layout.setSpacing(0)

            btn = QPushButton(month_label(key))
            btn.setCheckable(True)
            btn.setFixedHeight(32)
            btn.clicked.connect(lambda checked, k=key: self._on_btn_clicked(k))

            del_btn = QPushButton("✕")
            del_btn.setFixedSize(20, 20)
            del_btn.setToolTip("Monat löschen")
            del_btn.setCursor(Qt.PointingHandCursor)
            del_btn.setFlat(True)
            del_btn.clicked.connect(lambda checked, k=key: self.month_delete_requested.emit(k))

            row_layout.addWidget(btn)
            row_layout.addWidget(del_btn)

            self._layout.insertWidget(insert_at, row)
            self._rows[key] = row
            self._buttons[key] = btn
            insert_at += 1

        target = select_key if select_key in self._buttons else (
            self._selected if self._selected in self._buttons else keys[-1] if keys else None
        )
        if target:
            self._highlight(target)

        self.apply_theme(theme_manager.current)

    def _on_btn_clicked(self, key: str):
        self._highlight(key)
        self.month_selected.emit(key)

    def _highlight(self, key: str):
        self._selected = key
        for k, btn in self._buttons.items():
            btn.setChecked(k == key)

    def apply_theme(self, t: Theme):
        self.setStyleSheet(f"background: {t.nav_hover}; border-right: 1px solid {t.sidebar_border};")
        self._header.setStyleSheet(
            f"background: transparent; color: {t.content_text}; font-weight: bold; font-size: 13px; padding: 4px 6px 8px 6px;"
        )
        self._add_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent; color: {t.nav_active_text};
                border: 1px solid {t.nav_active_text}; border-radius: 6px; font-size: 12px;
            }}
            QPushButton:hover {{ background: {t.nav_active_bg}; }}
        """)
        for key, row in self._rows.items():
            self._buttons[key].setStyleSheet(f"""
                QPushButton {{
                    text-align: left; padding-left: 10px; border: none;
                    border-radius: 6px; font-size: 13px;
                    color: {t.content_text}; background: transparent;
                }}
                QPushButton:hover {{ background: {t.sidebar_border}; }}
                QPushButton:checked {{
                    background: {t.nav_active_bg}; color: {t.nav_active_text}; font-weight: bold;
                }}
            """)
            del_btn = row.layout().itemAt(1).widget()
            del_btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {t.version_text};
                    border: none;
                    border-radius: 10px;
                    font-size: 11px;
                    font-weight: bold;
                    padding: 0;
                }}
                QPushButton:hover {{
                    background: #e06c75;
                    color: white;
                }}
            """)


class DayTable(QWidget):
    def __init__(self):
        super().__init__()
        self._month_key: str = current_month_key()
        self._blocking = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self._title = QLabel()
        layout.addWidget(self._title)

        # Error panel (hidden by default)
        self._error_expanded = False
        self._error_items: list[str] = []

        self._error_panel = QFrame()
        self._error_panel.setFrameShape(QFrame.NoFrame)
        self._error_panel.setVisible(False)
        ep_layout = QVBoxLayout(self._error_panel)
        ep_layout.setContentsMargins(12, 8, 12, 8)
        ep_layout.setSpacing(4)

        header_row = QHBoxLayout()
        self._error_header = QLabel("⚠  Ungültige Fahrstrecken:")
        header_row.addWidget(self._error_header)
        header_row.addStretch()
        self._error_toggle = QPushButton()
        self._error_toggle.setFlat(True)
        self._error_toggle.setFixedSize(80, 22)
        self._error_toggle.setCursor(Qt.PointingHandCursor)
        self._error_toggle.setVisible(False)
        self._error_toggle.clicked.connect(self._toggle_errors)
        header_row.addWidget(self._error_toggle)
        ep_layout.addLayout(header_row)

        self._error_list = QLabel()
        self._error_list.setWordWrap(True)
        ep_layout.addWidget(self._error_list)
        layout.addWidget(self._error_panel)

        self._table = QTableWidget(0, 4)
        self._table.setHorizontalHeaderLabels(["Datum", "Ort / Route", "Fahrstrecke", "Hin & Zurück"])
        self._table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self._table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self._table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self._table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self._table.verticalHeader().setVisible(False)
        self._table.setShowGrid(False)
        self._table.setAlternatingRowColors(True)
        self._table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._table.cellChanged.connect(self._on_cell_changed)
        layout.addWidget(self._table)

        self.apply_theme(theme_manager.current)

    def load_month(self, key: str, entries: list[Entry]):
        self._month_key = key
        if not key or "." not in key:
            return
        self._title.setText(month_label(key))

        month, year = int(key.split(".")[0]), int(key.split(".")[1])
        days_in_month = calendar.monthrange(year, month)[1]
        entry_map = {e.date: e for e in entries}

        self._blocking = True
        self._table.setRowCount(0)
        today = date.today()

        for day in range(1, days_in_month + 1):
            d = date(year, month, day)
            date_str = d.strftime("%d.%m.%y")
            row = self._table.rowCount()
            self._table.insertRow(row)
            self._table.setRowHeight(row, 30)

            date_item = QTableWidgetItem(date_str)
            date_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self._table.setItem(row, 0, date_item)

            entry = entry_map.get(date_str)
            km_val = entry.km if entry else ""
            round_trip = self._calc_round_trip(km_val)

            self._table.setItem(row, 1, QTableWidgetItem(entry.location if entry else ""))
            self._table.setItem(row, 2, QTableWidgetItem(km_val))

            rt_item = QTableWidgetItem(round_trip)
            rt_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self._table.setItem(row, 3, rt_item)

            if d.weekday() >= 5:
                for col in range(4):
                    item = self._table.item(row, col)
                    if item:
                        item.setForeground(QColor("#aaaaaa"))

            if d == today:
                f = QFont()
                f.setBold(True)
                for col in range(4):
                    item = self._table.item(row, col)
                    if item:
                        item.setFont(f)

        self._blocking = False
        self._validate_errors()
        self.apply_theme(theme_manager.current)

    @staticmethod
    def _calc_round_trip(km_str: str) -> str:
        try:
            return str(int(km_str.strip()) * 2)
        except (ValueError, AttributeError):
            return ""

    def _on_cell_changed(self, row: int, col: int):
        if self._blocking or col == 0 or col == 3:
            return
        date_item = self._table.item(row, 0)
        loc_item = self._table.item(row, 1)
        km_item = self._table.item(row, 2)
        if not date_item:
            return

        date_str = date_item.text()
        location = (loc_item.text().strip() if loc_item else "")
        km = (km_item.text().strip() if km_item else "")

        if col == 2:
            self._blocking = True
            rt_item = self._table.item(row, 3)
            if rt_item:
                rt_item.setText(self._calc_round_trip(km))
            self._blocking = False
            self._validate_errors()

        data = load_data()
        entries = data.get(self._month_key, [])
        existing = next((e for e in entries if e.date == date_str), None)

        if location or km:
            if existing:
                existing.location = location
                existing.km = km
            else:
                entries.append(Entry(date=date_str, location=location, km=km))
        elif existing:
            entries.remove(existing)

        data[self._month_key] = entries
        save_data(data)

    def _toggle_errors(self):
        self._error_expanded = not self._error_expanded
        self._render_errors()

    def _render_errors(self):
        MAX = 4
        errors = self._error_items
        has_more = len(errors) > MAX
        self._error_toggle.setVisible(has_more)
        if has_more:
            self._error_toggle.setText("▲ Weniger" if self._error_expanded else f"▼ Alle ({len(errors)})")
        shown = errors if self._error_expanded else errors[:MAX]
        self._error_list.setText("\n".join(f"  • {e}" for e in shown))
        self.apply_theme(theme_manager.current)

    def _validate_errors(self):
        errors = []
        for row in range(self._table.rowCount()):
            km_item = self._table.item(row, 2)
            date_item = self._table.item(row, 0)
            if not km_item or not date_item:
                continue
            km = km_item.text().strip()
            if km and not km.lstrip("-").isdigit():
                errors.append(f"{date_item.text()}  →  \"{km}\"")

        self._error_items = errors
        self._error_expanded = False
        if errors:
            self._render_errors()
            self._error_panel.setVisible(True)
        else:
            self._error_panel.setVisible(False)

    def focus_date(self, date_str: str):
        for row in range(self._table.rowCount()):
            item = self._table.item(row, 0)
            if item and item.text() == date_str:
                self._table.selectRow(row)
                self._table.scrollToItem(item)
                self._table.setCurrentCell(row, 1)
                break

    def apply_theme(self, t: Theme):
        bg, text, border, hover, accent = (
            t.content_bg, t.content_text, t.sidebar_border, t.nav_hover, t.nav_active_text
        )
        self.setStyleSheet(f"background: {bg};")
        self._title.setStyleSheet(f"background: transparent; color: {text}; font-size: 18px; font-weight: bold;")
        self._error_panel.setStyleSheet(f"""
            QFrame {{ background: #fff3cd; border: 1px solid #f0ad4e; border-radius: 6px; }}
        """)
        self._error_header.setStyleSheet("background: transparent; border: none; color: #856404; font-weight: bold; font-size: 12px;")
        self._error_list.setStyleSheet("background: transparent; border: none; color: #856404; font-size: 12px;")
        self._error_toggle.setStyleSheet("""
            QPushButton { background: transparent; color: #856404; border: 1px solid #f0ad4e; border-radius: 4px; font-size: 11px; }
            QPushButton:hover { background: #f0ad4e; color: white; }
        """)
        self._table.setStyleSheet(f"""
            QTableWidget {{
                background: {bg}; color: {text}; border: 1px solid {border};
                border-radius: 8px; font-size: 13px; gridline-color: transparent;
            }}
            QTableWidget::item {{ padding: 2px 12px; border: none; }}
            QTableWidget::item:selected {{ background: {t.nav_active_bg}; color: {accent}; }}
            QHeaderView::section {{
                background: {hover}; color: {text}; border: none;
                padding: 6px 12px; font-weight: bold; font-size: 12px;
            }}
            QTableWidget::item:alternate {{ background: {hover}; }}
            QLineEdit {{
                background: {bg}; color: {text};
                border: 1px solid {accent}; border-radius: 0;
                padding: 0 10px; font-size: 13px;
            }}
        """)

        scrollbar_style = f"""
            QScrollBar:vertical {{
                background: {hover};
                width: 8px;
                margin: 6px 2px;
                border-radius: 4px;
                border: none;
            }}
            QScrollBar::handle:vertical {{
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 {t.title_color},
                    stop:1 {accent}
                );
                border-radius: 4px;
                min-height: 28px;
                margin: 0;
            }}
            QScrollBar::handle:vertical:hover {{
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 {accent},
                    stop:1 {t.title_color}
                );
            }}
            QScrollBar::handle:vertical:pressed {{
                background: {accent};
            }}
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                height: 0; border: none; background: transparent;
            }}
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {{
                background: transparent;
            }}
        """
        self._table.verticalScrollBar().setStyleSheet(scrollbar_style)


class EntryView(QWidget):
    def __init__(self):
        super().__init__()
        self._data: dict[str, list[Entry]] = load_data()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._month_list = MonthList()
        self._month_list.setFixedWidth(150)
        self._month_list.month_selected.connect(self._load_month)
        self._month_list._add_btn.clicked.connect(self._add_next_month)
        self._month_list.month_delete_requested.connect(self._delete_month)
        layout.addWidget(self._month_list)

        self._day_table = DayTable()
        layout.addWidget(self._day_table)

        self._init_months()
        theme_manager.changed.connect(self._on_theme_change)

    def _init_months(self):
        if not self._data:
            key = current_month_key()
            self._data[key] = []
            save_data(self._data)
        keys = sorted(self._data.keys())
        self._month_list.populate(keys, select_key=keys[-1])
        self._load_month(keys[-1])

    def _add_next_month(self):
        keys = sorted(self._data.keys())
        if keys:
            last = keys[-1]
            m, y = int(last.split(".")[0]), int(last.split(".")[1])
            m += 1
            if m > 12:
                m, y = 1, y + 1
            default_key = f"{m:02d}.{y}"
        else:
            default_key = current_month_key()

        dlg = MonthPickerDialog(default_key, keys, parent=self)
        if dlg.exec() != QDialog.Accepted:
            return

        new_key = dlg.result_key()
        if new_key not in self._data:
            self._data[new_key] = []
            save_data(self._data)

        keys = sorted(self._data.keys())
        self._month_list.populate(keys, select_key=new_key)
        self._load_month(new_key)

    def _delete_month(self, key: str):
        from PySide6.QtWidgets import QMessageBox
        t = theme_manager.current
        msg = QMessageBox(self)
        msg.setWindowTitle("Monat löschen")
        msg.setText(f"{month_label(key)} wirklich löschen?")
        msg.setInformativeText("Alle Einträge dieses Monats werden gelöscht.")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.setStyleSheet(f"""
            QMessageBox {{ background: {t.content_bg}; }}
            QLabel {{ color: {t.content_text}; background: transparent; }}
        """)
        msg.button(QMessageBox.Yes).setStyleSheet(f"""
            QPushButton {{
                background: #e06c75; color: white; border: none;
                border-radius: 6px; padding: 6px 18px; font-size: 13px; min-width: 80px;
            }}
            QPushButton:hover {{ background: #c0535e; }}
        """)
        msg.button(QMessageBox.Cancel).setStyleSheet(f"""
            QPushButton {{
                background: {t.nav_hover}; color: {t.content_text};
                border: 1px solid {t.sidebar_border}; border-radius: 6px;
                padding: 6px 18px; font-size: 13px; min-width: 80px;
            }}
            QPushButton:hover {{ background: {t.sidebar_border}; }}
        """)
        if msg.exec() != QMessageBox.Yes:
            return

        self._data.pop(key, None)
        save_data(self._data)

        keys = sorted(self._data.keys())
        if keys:
            self._month_list.populate(keys, select_key=keys[-1])
            self._load_month(keys[-1])
        else:
            self._month_list.populate([])
            self._day_table._table.setRowCount(0)
            self._day_table._title.setText("")

    def _load_month(self, key: str):
        if not key or "." not in key:
            return
        self._data = load_data()
        self._day_table.load_month(key, self._data.get(key, []))

    def navigate_to(self, month_key: str, date_str: str):
        self._data = load_data()
        if month_key not in self._data:
            self._data[month_key] = []
            save_data(self._data)
        keys = sorted(self._data.keys())
        self._month_list.populate(keys, select_key=month_key)
        self._day_table.load_month(month_key, self._data.get(month_key, []))
        self._day_table.focus_date(date_str)

    def _on_theme_change(self, t: Theme):
        self._month_list.apply_theme(t)
        self._day_table.apply_theme(t)

    def apply_theme(self, t: Theme):
        self._month_list.apply_theme(t)
        self._day_table.apply_theme(t)
