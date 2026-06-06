from collections import Counter
from datetime import date

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QSizePolicy, QScrollArea,
)
from PySide6.QtCharts import (
    QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter

from src.models import load_data, month_label
from src.theme import theme_manager, Theme


MONTH_SHORT = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun",
               "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]


def _km_int(km_str: str) -> int:
    try:
        return int(km_str.strip())
    except (ValueError, AttributeError):
        return 0


class StatCard(QFrame):
    def __init__(self, title: str):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(2)

        self._title_lbl = QLabel(title)
        self._value_lbl = QLabel("—")

        layout.addWidget(self._title_lbl)
        layout.addWidget(self._value_lbl)

    def set_value(self, value: str):
        self._value_lbl.setText(value)

    def apply_theme(self, t: Theme):
        self.setStyleSheet(f"""
            QFrame {{
                background: {t.nav_hover};
                border: 1px solid {t.sidebar_border};
                border-radius: 10px;
            }}
        """)
        self._title_lbl.setStyleSheet(
            f"background: transparent; border: none; "
            f"color: {t.version_text}; font-size: 12px;"
        )
        self._value_lbl.setStyleSheet(
            f"background: transparent; border: none; "
            f"color: {t.content_text}; font-size: 22px; font-weight: bold;"
        )


class AnalyseView(QWidget):
    def __init__(self):
        super().__init__()
        self._year = date.today().year

        # ── Outer scroll so it works on small windows ──────────────
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        outer.addWidget(scroll)

        inner = QWidget()
        scroll.setWidget(inner)

        layout = QVBoxLayout(inner)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)

        # ── Header + year selector ─────────────────────────────────
        header = QHBoxLayout()

        self._title_lbl = QLabel("Analyse")
        self._title_lbl.setStyleSheet("font-size: 20px; font-weight: bold;")
        header.addWidget(self._title_lbl)
        header.addStretch()

        self._prev_btn = QPushButton("◀")
        self._prev_btn.setFixedSize(30, 30)
        self._prev_btn.clicked.connect(self._prev_year)

        self._year_lbl = QLabel(str(self._year))
        self._year_lbl.setFixedWidth(52)
        self._year_lbl.setAlignment(Qt.AlignCenter)

        self._next_btn = QPushButton("▶")
        self._next_btn.setFixedSize(30, 30)
        self._next_btn.clicked.connect(self._next_year)

        header.addWidget(self._prev_btn)
        header.addWidget(self._year_lbl)
        header.addWidget(self._next_btn)
        layout.addLayout(header)

        # ── Stat cards ─────────────────────────────────────────────
        cards = QHBoxLayout()
        cards.setSpacing(12)

        self._card_total  = StatCard("Gesamt km (H & Z)")
        self._card_avg    = StatCard("Ø km / Monat")
        self._card_route  = StatCard("Häufigste Route")
        self._card_best   = StatCard("Stärkster Monat")

        for c in (self._card_total, self._card_avg, self._card_route, self._card_best):
            cards.addWidget(c)
        layout.addLayout(cards)

        # ── Bar chart ──────────────────────────────────────────────
        self._chart_title = QLabel("Monatliche Kilometerlauf (Hin & Zurück)")
        layout.addWidget(self._chart_title)

        self._chart = QChart()
        self._chart.setAnimationOptions(QChart.SeriesAnimations)
        self._chart.legend().setVisible(False)
        self._chart.setMargins(__import__("PySide6.QtCore", fromlist=["QMargins"]).QMargins(8, 8, 8, 8))

        self._chart_view = QChartView(self._chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)
        self._chart_view.setMinimumHeight(260)
        layout.addWidget(self._chart_view)

        # ── Route breakdown ────────────────────────────────────────
        self._route_title = QLabel("Routen – Jahresübersicht")
        layout.addWidget(self._route_title)

        self._route_table = QTableWidget(0, 3)
        self._route_table.setHorizontalHeaderLabels(["Route", "Fahrten", "km gesamt (H & Z)"])
        self._route_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self._route_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self._route_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self._route_table.verticalHeader().setVisible(False)
        self._route_table.setShowGrid(False)
        self._route_table.setAlternatingRowColors(True)
        self._route_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._route_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._route_table.setMinimumHeight(200)
        layout.addWidget(self._route_table)

        layout.addStretch()

        theme_manager.changed.connect(self._on_theme_change)
        self.apply_theme(theme_manager.current)

    # ── Public ────────────────────────────────────────────────────
    def refresh(self):
        data = load_data()
        year_data = {k: v for k, v in data.items() if k.endswith(f".{self._year}")}
        self._update_stats(year_data)
        self._update_chart(year_data)
        self._update_route_table(year_data)

    def apply_theme(self, t: Theme):
        self.setStyleSheet(f"background: {t.content_bg};")

        scroll = self.findChild(QScrollArea)
        if scroll:
            scroll.setStyleSheet(f"""
                QScrollArea {{ background: {t.content_bg}; border: none; }}
                QWidget {{ background: {t.content_bg}; }}
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

        self._title_lbl.setStyleSheet(
            f"background: transparent; color: {t.content_text}; "
            f"font-size: 20px; font-weight: bold;"
        )
        self._chart_title.setStyleSheet(
            f"background: transparent; color: {t.content_text}; "
            f"font-size: 13px; font-weight: bold;"
        )
        self._route_title.setStyleSheet(
            f"background: transparent; color: {t.content_text}; "
            f"font-size: 13px; font-weight: bold;"
        )

        nav_style = f"""
            QPushButton {{
                background: {t.nav_hover}; color: {t.content_text};
                border: 1px solid {t.sidebar_border}; border-radius: 6px;
                font-size: 12px; font-weight: bold;
            }}
            QPushButton:hover {{ background: {t.sidebar_border}; }}
        """
        self._prev_btn.setStyleSheet(nav_style)
        self._next_btn.setStyleSheet(nav_style)
        self._year_lbl.setStyleSheet(
            f"background: transparent; color: {t.content_text}; "
            f"font-size: 14px; font-weight: bold;"
        )

        for card in (self._card_total, self._card_avg, self._card_route, self._card_best):
            card.apply_theme(t)

        self._route_table.setStyleSheet(f"""
            QTableWidget {{
                background: {t.content_bg}; color: {t.content_text};
                border: 1px solid {t.sidebar_border};
                border-radius: 8px; font-size: 13px; gridline-color: transparent;
            }}
            QTableWidget::item {{ padding: 4px 14px; border: none; }}
            QTableWidget::item:selected {{ background: {t.nav_active_bg}; color: {t.nav_active_text}; }}
            QTableWidget::item:alternate {{ background: {t.nav_hover}; }}
            QHeaderView::section {{
                background: {t.nav_hover}; color: {t.content_text};
                border: none; padding: 6px 12px;
                font-weight: bold; font-size: 12px;
            }}
        """)

        # Rebuild chart with new theme colors
        self.refresh()

    # ── Private ───────────────────────────────────────────────────
    def _update_stats(self, year_data: dict):
        all_entries = [e for entries in year_data.values() for e in entries]

        total_km = sum(_km_int(e.km) * 2 for e in all_entries)

        months_with_km = [k for k, v in year_data.items()
                          if any(_km_int(e.km) > 0 for e in v)]
        avg_km = round(total_km / len(months_with_km)) if months_with_km else 0

        location_counts = Counter(e.location for e in all_entries if e.location)
        top_route = location_counts.most_common(1)[0][0] if location_counts else "—"

        best_key = max(
            year_data.keys(),
            key=lambda k: sum(_km_int(e.km) * 2 for e in year_data[k]),
            default=None,
        )
        best_month = month_label(best_key) if best_key else "—"

        self._card_total.set_value(f"{total_km:,} km".replace(",", "."))
        self._card_avg.set_value(f"{avg_km} km")
        self._card_route.set_value(top_route if top_route else "—")
        self._card_best.set_value(best_month)

    def _update_chart(self, year_data: dict):
        self._chart.removeAllSeries()
        for axis in self._chart.axes():
            self._chart.removeAxis(axis)

        t = theme_manager.current

        bar_color   = "#89b4fa" if t.name == "dark" else t.nav_active_text
        label_color = "#1e1e2e" if t.name == "dark" else "#ffffff"

        bar_set = QBarSet("km")
        bar_set.setColor(QColor(bar_color))
        bar_set.setBorderColor(Qt.transparent)
        bar_set.setLabelColor(QColor(label_color))

        monthly_km: list[int] = []
        for m in range(1, 13):
            key = f"{m:02d}.{self._year}"
            km = sum(_km_int(e.km) * 2 for e in year_data.get(key, []))
            bar_set.append(km)
            monthly_km.append(km)

        series = QBarSeries()
        series.append(bar_set)
        series.setLabelsVisible(True)
        series.setLabelsPosition(QBarSeries.LabelsInsideEnd)
        self._chart.addSeries(series)

        x_axis = QBarCategoryAxis()
        x_axis.append(MONTH_SHORT)
        x_axis.setLabelsColor(QColor(t.content_text))
        x_axis.setLinePen(QColor(t.sidebar_border))
        x_axis.setGridLinePen(QColor(t.sidebar_border))

        max_val = max(monthly_km) if any(monthly_km) else 100
        y_axis = QValueAxis()
        y_axis.setRange(0, max_val * 1.18)
        y_axis.setLabelFormat("%d km")
        y_axis.setLabelsColor(QColor(t.content_text))
        y_axis.setGridLineColor(QColor(t.sidebar_border))
        y_axis.setMinorGridLineVisible(False)
        y_axis.setTickCount(5)

        self._chart.addAxis(x_axis, Qt.AlignBottom)
        self._chart.addAxis(y_axis, Qt.AlignLeft)
        series.attachAxis(x_axis)
        series.attachAxis(y_axis)

        self._chart.setBackgroundBrush(QColor(t.content_bg))
        self._chart.setBackgroundPen(Qt.NoPen)
        self._chart.setPlotAreaBackgroundBrush(QColor(t.content_bg))
        self._chart.setPlotAreaBackgroundVisible(True)

        self._chart_view.setStyleSheet(
            f"background: {t.content_bg}; "
            f"border: 1px solid {t.sidebar_border}; border-radius: 10px;"
        )

    def _update_route_table(self, year_data: dict):
        all_entries = [e for entries in year_data.values() for e in entries]

        route_km: dict[str, int] = {}
        route_count: dict[str, int] = {}
        for e in all_entries:
            if not e.location:
                continue
            route_km[e.location]    = route_km.get(e.location, 0)    + _km_int(e.km) * 2
            route_count[e.location] = route_count.get(e.location, 0) + 1

        routes = sorted(route_km, key=lambda r: route_km[r], reverse=True)
        self._route_table.setRowCount(len(routes))

        for i, route in enumerate(routes):
            self._route_table.setItem(i, 0, QTableWidgetItem(route))

            count_item = QTableWidgetItem(str(route_count[route]))
            count_item.setTextAlignment(Qt.AlignCenter)
            self._route_table.setItem(i, 1, count_item)

            km_item = QTableWidgetItem(f"{route_km[route]} km")
            km_item.setTextAlignment(Qt.AlignCenter)
            self._route_table.setItem(i, 2, km_item)

            self._route_table.setRowHeight(i, 34)

    def _prev_year(self):
        self._year -= 1
        self._year_lbl.setText(str(self._year))
        self.refresh()

    def _next_year(self):
        self._year += 1
        self._year_lbl.setText(str(self._year))
        self.refresh()

    def _on_theme_change(self, t: Theme):
        self.apply_theme(t)
