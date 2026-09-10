from PySide6.QtCore import QObject

from ..database import SessionLocal
from ..services.settings import get_setting, set_setting


THEMES = {
    "MODERN_BLUE": {
        "label": "Modern Blue",
        "stylesheet": """
            QWidget { background: #f4f7fb; color: #172033; font-family: 'Segoe UI'; }
            QMainWindow, QDialog { background: #f4f7fb; }
            QMenuBar { background: #ffffff; color: #344054; border-bottom: 1px solid #d9e2ec; padding: 3px; }
            QMenuBar::item:selected, QMenu::item:selected { background: #e8f1fb; color: #145a96; }
            QMenu { background: #ffffff; color: #172033; border: 1px solid #d9e2ec; }
            QTabWidget::pane { border: 0; background: #f4f7fb; }
            QTabBar { background: #edf2f7; }
            QTabBar::tab { background: #edf2f7; color: #526070; padding: 10px 16px; border: 0; }
            QTabBar::tab:hover { background: #ffffff; color: #145a96; }
            QTabBar::tab:selected { background: #ffffff; color: #145a96; border-bottom: 3px solid #2673b8; }
            QPushButton { background: #2673b8; color: white; border: 0; border-radius: 7px; padding: 8px 14px; font-weight: 600; }
            QPushButton:hover { background: #1f5f99; }
            QPushButton:disabled { background: #cbd5e1; color: #64748b; }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit { background: white; color: #172033; border: 1px solid #cbd5e1; border-radius: 6px; padding: 6px; }
            QTableWidget, QListWidget { background: white; color: #172033; border: 1px solid #d9e2ec; border-radius: 8px; alternate-background-color: #f8fafc; }
            QHeaderView::section { background: #e8f0f8; color: #17324d; padding: 8px; border: 0; font-weight: 700; }
            QGroupBox { background: white; border: 1px solid #d9e2ec; border-radius: 9px; margin-top: 10px; padding: 12px 8px 8px; font-weight: 700; }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; background: #f4f7fb; }
        """,
    },
    "KEMERDEKAAN": {
        "label": "Kemerdekaan",
        "stylesheet": """
            QWidget { background: #f8fafc; color: #202124; font-family: 'Segoe UI'; }
            QMainWindow, QDialog { background: #f8fafc; }
            QMenuBar { background: #ffffff; color: #202124; border-bottom: 2px solid #c62828; }
            QMenuBar::item:selected, QMenu::item:selected { background: #fff1f1; color: #b71c1c; }
            QMenu { background: #ffffff; color: #202124; border: 1px solid #e0e0e0; }
            QTabWidget::pane { border: 0; background: #f8fafc; }
            QTabBar { background: #fff5f5; }
            QTabBar::tab { background: #fff5f5; color: #7f1d1d; padding: 10px 16px; border: 0; }
            QTabBar::tab:selected { background: #ffffff; color: #b71c1c; border-bottom: 3px solid #d32f2f; }
            QPushButton { background: #c62828; color: white; border: 0; border-radius: 7px; padding: 8px 14px; font-weight: 700; }
            QPushButton:hover { background: #a91f1f; }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit { background: white; color: #202124; border: 1px solid #d6d6d6; border-radius: 6px; padding: 6px; }
            QTableWidget, QListWidget { background: white; color: #202124; border: 1px solid #e0e0e0; border-radius: 8px; alternate-background-color: #fffafa; }
            QHeaderView::section { background: #fde8e8; color: #8f1d1d; padding: 8px; border: 0; font-weight: 700; }
            QGroupBox { background: white; border: 1px solid #e6d5d5; border-radius: 9px; margin-top: 10px; padding: 12px 8px 8px; font-weight: 700; }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; background: #f8fafc; color: #b71c1c; }
        """,
    },
    "KEAGAMAAN": {
        "label": "Keagamaan",
        "stylesheet": """
            QWidget { background: #f5f7f4; color: #203027; font-family: 'Segoe UI'; }
            QMainWindow, QDialog { background: #f5f7f4; }
            QMenuBar { background: #ffffff; color: #294638; border-bottom: 2px solid #5f7f68; }
            QMenuBar::item:selected, QMenu::item:selected { background: #edf4ee; color: #315a40; }
            QMenu { background: #ffffff; color: #203027; border: 1px solid #d7e2d9; }
            QTabWidget::pane { border: 0; background: #f5f7f4; }
            QTabBar { background: #edf2ed; }
            QTabBar::tab { background: #edf2ed; color: #50675a; padding: 10px 16px; border: 0; }
            QTabBar::tab:selected { background: #ffffff; color: #315a40; border-bottom: 3px solid #66856f; }
            QPushButton { background: #587963; color: white; border: 0; border-radius: 7px; padding: 8px 14px; font-weight: 600; }
            QPushButton:hover { background: #476650; }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit { background: white; color: #203027; border: 1px solid #ccd8ce; border-radius: 6px; padding: 6px; }
            QTableWidget, QListWidget { background: white; color: #203027; border: 1px solid #d7e2d9; border-radius: 8px; alternate-background-color: #fafcf9; }
            QHeaderView::section { background: #e7efe9; color: #315a40; padding: 8px; border: 0; font-weight: 700; }
            QGroupBox { background: white; border: 1px solid #d7e2d9; border-radius: 9px; margin-top: 10px; padding: 12px 8px 8px; font-weight: 700; }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; background: #f5f7f4; color: #315a40; }
        """,
    },
    "DARK": {
        "label": "Dark Mode",
        "stylesheet": """
            QWidget { background: #171a21; color: #e6eaf0; font-family: 'Segoe UI'; }
            QMainWindow, QDialog { background: #171a21; }
            QMenuBar { background: #11141a; color: #e6eaf0; border-bottom: 1px solid #303641; }
            QMenuBar::item:selected, QMenu::item:selected { background: #293241; color: #ffffff; }
            QMenu { background: #1e232d; color: #e6eaf0; border: 1px solid #3a424f; }
            QTabWidget::pane { border: 0; background: #171a21; }
            QTabBar { background: #11141a; }
            QTabBar::tab { background: #11141a; color: #aab3c0; padding: 10px 16px; border: 0; }
            QTabBar::tab:hover { background: #222833; color: white; }
            QTabBar::tab:selected { background: #1e232d; color: #ffffff; border-bottom: 3px solid #6ea8fe; }
            QPushButton { background: #315f9f; color: white; border: 0; border-radius: 7px; padding: 8px 14px; font-weight: 600; }
            QPushButton:hover { background: #3d73bd; }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit { background: #222833; color: #e6eaf0; border: 1px solid #3a424f; border-radius: 6px; padding: 6px; }
            QTableWidget, QListWidget { background: #1e232d; color: #e6eaf0; border: 1px solid #343c49; border-radius: 8px; alternate-background-color: #222833; }
            QHeaderView::section { background: #293241; color: #e6eaf0; padding: 8px; border: 0; font-weight: 700; }
            QGroupBox { background: #1e232d; border: 1px solid #343c49; border-radius: 9px; margin-top: 10px; padding: 12px 8px 8px; font-weight: 700; }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; background: #171a21; color: #cbd5e1; }
        """,
    },
}


def current_theme():
    with SessionLocal() as session:
        return get_setting(session, "ui_theme", "MODERN_BLUE")


def set_theme(theme_key):
    if theme_key not in THEMES:
        raise ValueError("Tema tidak tersedia")
    with SessionLocal() as session:
        set_setting(session, "ui_theme", theme_key)


def apply_theme(app, theme_key):
    theme = THEMES.get(theme_key, THEMES["MODERN_BLUE"])
    app.setStyleSheet(theme["stylesheet"])
    return theme["label"]
