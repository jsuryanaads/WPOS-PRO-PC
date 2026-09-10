from ..database import SessionLocal
from ..services.settings import get_setting, set_setting


COMMON = """
    QLabel#pageTitle { font-size: 24px; font-weight: 800; }
    QLabel#pageSubtitle { font-size: 13px; }
    QFrame#card { border-radius: 10px; }
    QLabel#cardTitle { font-size: 11px; font-weight: 700; }
    QLabel#cardValue { font-size: 22px; font-weight: 800; }
    QFrame#brandStrip { border-radius: 11px; }
    QLabel#brandName { font-size: 18px; font-weight: 800; background: transparent; }
    QLabel#brandVersion { font-size: 11px; background: transparent; }
    QLabel#total { border-radius: 8px; padding: 10px 14px; font-size: 18px; font-weight: 800; }
    QFrame#loginCard { border-radius: 18px; }
    QLabel#loginTitle { font-size: 27px; font-weight: 800; }
    QLabel#loginVersion { font-size: 12px; }
    QLabel#loginWelcome { font-size: 13px; }
    QLabel#loginFieldLabel { font-size: 11px; font-weight: 800; }
    QLabel#loginFooter { font-size: 11px; }
    QLineEdit#loginInput { min-height: 30px; padding: 6px 12px; border-radius: 9px; }
    QPushButton#loginPrimaryButton { min-height: 30px; border-radius: 10px; font-size: 14px; font-weight: 800; }
    QPushButton#loginSecondaryButton { min-width: 58px; min-height: 30px; border-radius: 9px; font-weight: 700; }
"""

THEMES = {
    "MODERN_BLUE": {
        "label": "Modern Blue",
        "stylesheet": COMMON + """
            QWidget { background: #f5f7fb; color: #1f2937; font-family: 'Segoe UI'; }
            QMainWindow, QDialog { background: #f5f7fb; }
            QMenuBar { background: #ffffff; color: #344054; border-bottom: 1px solid #d9e2ec; }
            QMenuBar::item:selected, QMenu::item:selected { background: #e8f1fb; color: #145a96; }
            QMenu { background: #ffffff; color: #172033; border: 1px solid #d9e2ec; }
            QTabWidget::pane { border: 0; background: #f5f7fb; }
            QTabBar { background: #edf2f7; }
            QTabBar::tab { background: #edf2f7; color: #526070; padding: 10px 16px; border: 0; }
            QTabBar::tab:hover { background: #ffffff; color: #145a96; }
            QTabBar::tab:selected { background: #ffffff; color: #145a96; border-bottom: 3px solid #2673b8; }
            QPushButton { background: #3b78a8; color: white; border: 0; border-radius: 7px; padding: 8px 14px; font-weight: 600; }
            QPushButton:hover { background: #2f638e; }
            QPushButton:disabled { background: #cbd5e1; color: #64748b; }
            QPushButton#primary { background: #2673b8; }
            QPushButton#danger { background: #b54747; }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit { background: white; color: #172033; border: 1px solid #cbd5e1; border-radius: 6px; padding: 6px; }
            QTableWidget, QListWidget { background: white; color: #172033; border: 1px solid #d9e2ec; border-radius: 8px; alternate-background-color: #f8fafc; }
            QHeaderView::section { background: #e8f0f8; color: #17324d; padding: 8px; border: 0; font-weight: 700; }
            QGroupBox { background: white; border: 1px solid #d9e2ec; border-radius: 9px; margin-top: 10px; padding: 12px 8px 8px; font-weight: 700; }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; background: #f5f7fb; color: #315a7d; }
            QFrame#brandStrip { background: #2673b8; }
            QLabel#brandName, QLabel#brandVersion { color: white; }
            QLabel#cardTitle { color: #718096; }
            QLabel#cardValue { color: #102a43; }
            QLabel#total { background: #245d88; color: white; }
            QFrame#loginCard { background: #ffffff; border: 1px solid #d9e2ec; }
            QLabel#loginTitle { color: #172033; }
            QLabel#loginVersion, QLabel#loginWelcome, QLabel#loginFieldLabel, QLabel#loginFooter { color: #64748b; }
            QPushButton#loginPrimaryButton { background: #2673b8; color: #ffffff; }
            QPushButton#loginPrimaryButton:hover { background: #1f5f99; }
            QPushButton#loginSecondaryButton { background: #e8f1fb; color: #145a96; }
            QPushButton#loginSecondaryButton:hover { background: #dbeafe; }
        """,
    },
    "KEMERDEKAAN": {
        "label": "Kemerdekaan",
        "stylesheet": COMMON + """
            QWidget { background: #f0e8e8; color: #2b2020; font-family: 'Segoe UI'; }
            QMainWindow, QDialog { background: #f0e8e8; }
            QMenuBar { background: #7f1d1d; color: #fff7f7; border-bottom: 2px solid #c43f3f; }
            QMenuBar::item:selected { background: #a52b2b; color: #ffffff; }
            QMenu { background: #7f1d1d; color: #ffffff; border: 1px solid #b23a3a; }
            QMenu::item:selected { background: #b93434; color: #ffffff; }
            QTabWidget::pane { border: 0; background: #f0e8e8; }
            QTabBar { background: #8f2525; }
            QTabBar::tab { background: #8f2525; color: #ffe8e8; padding: 10px 16px; border: 0; }
            QTabBar::tab:hover { background: #a52b2b; color: #ffffff; }
            QTabBar::tab:selected { background: #f7eeee; color: #8f1d1d; border-bottom: 3px solid #d14343; }
            QPushButton { background: #a52f2f; color: #ffffff; border: 0; border-radius: 7px; padding: 8px 14px; font-weight: 700; }
            QPushButton:hover { background: #8f2525; }
            QPushButton:disabled { background: #c9aaaa; color: #f7eeee; }
            QPushButton#primary { background: #b93434; }
            QPushButton#danger { background: #7f1d1d; }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit { background: #fff7f7; color: #2b2020; border: 1px solid #d7b8b8; border-radius: 6px; padding: 6px; }
            QTableWidget, QListWidget { background: #fff7f7; color: #2b2020; border: 1px solid #d7b8b8; border-radius: 8px; alternate-background-color: #f7e9e9; }
            QHeaderView::section { background: #c43f3f; color: #ffffff; padding: 8px; border: 0; font-weight: 700; }
            QGroupBox { background: #f8eeee; border: 1px solid #d7b8b8; border-radius: 9px; margin-top: 10px; padding: 12px 8px 8px; font-weight: 700; }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; background: #f0e8e8; color: #8f1d1d; }
            QFrame#brandStrip { background: #9f2929; }
            QLabel#brandName, QLabel#brandVersion { color: white; }
            QLabel#cardTitle { color: #7f4545; }
            QLabel#cardValue { color: #5f2020; }
            QFrame#card { background: #f8eeee; border: 1px solid #d7b8b8; }
            QLabel#total { background: #8f2525; color: white; }
            QFrame#loginCard { background: #f8eeee; border: 1px solid #d7b8b8; }
            QLabel#loginTitle { color: #7f1d1d; }
            QLabel#loginVersion, QLabel#loginWelcome, QLabel#loginFieldLabel, QLabel#loginFooter { color: #7f4545; }
            QPushButton#loginPrimaryButton { background: #a52f2f; color: #ffffff; }
            QPushButton#loginPrimaryButton:hover { background: #8f2525; }
            QPushButton#loginSecondaryButton { background: #ead5d5; color: #7f1d1d; }
            QPushButton#loginSecondaryButton:hover { background: #e0c2c2; }
        """,
    },
    "KEAGAMAAN": {
        "label": "Keagamaan",
        "stylesheet": COMMON + """
            QWidget { background: #e8eee9; color: #203027; font-family: 'Segoe UI'; }
            QMainWindow, QDialog { background: #e8eee9; }
            QMenuBar { background: #294638; color: #f3f7f3; border-bottom: 2px solid #7c9a83; }
            QMenuBar::item:selected { background: #3d5f4a; color: #ffffff; }
            QMenu { background: #294638; color: #ffffff; border: 1px solid #55745f; }
            QMenu::item:selected { background: #4f705a; color: #ffffff; }
            QTabWidget::pane { border: 0; background: #e8eee9; }
            QTabBar { background: #365641; }
            QTabBar::tab { background: #365641; color: #e2eee5; padding: 10px 16px; border: 0; }
            QTabBar::tab:hover { background: #476650; color: #ffffff; }
            QTabBar::tab:selected { background: #eef3ef; color: #294638; border-bottom: 3px solid #718f78; }
            QPushButton { background: #52715c; color: #ffffff; border: 0; border-radius: 7px; padding: 8px 14px; font-weight: 600; }
            QPushButton:hover { background: #3f5e49; }
            QPushButton:disabled { background: #aebdb2; color: #eef3ef; }
            QPushButton#primary { background: #496c55; }
            QPushButton#danger { background: #855050; }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit { background: #f3f7f3; color: #203027; border: 1px solid #b8c9bb; border-radius: 6px; padding: 6px; }
            QTableWidget, QListWidget { background: #f3f7f3; color: #203027; border: 1px solid #b8c9bb; border-radius: 8px; alternate-background-color: #e5ede7; }
            QHeaderView::section { background: #587963; color: #ffffff; padding: 8px; border: 0; font-weight: 700; }
            QGroupBox { background: #eef3ef; border: 1px solid #b8c9bb; border-radius: 9px; margin-top: 10px; padding: 12px 8px 8px; font-weight: 700; }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; background: #e8eee9; color: #294638; }
            QFrame#brandStrip { background: #496b54; }
            QLabel#brandName, QLabel#brandVersion { color: white; }
            QLabel#cardTitle { color: #58705f; }
            QLabel#cardValue { color: #294638; }
            QFrame#card { background: #eef3ef; border: 1px solid #b8c9bb; }
            QLabel#total { background: #496c55; color: white; }
            QFrame#loginCard { background: #eef3ef; border: 1px solid #b8c9bb; }
            QLabel#loginTitle { color: #294638; }
            QLabel#loginVersion, QLabel#loginWelcome, QLabel#loginFieldLabel, QLabel#loginFooter { color: #58705f; }
            QPushButton#loginPrimaryButton { background: #496c55; color: #ffffff; }
            QPushButton#loginPrimaryButton:hover { background: #3f5e49; }
            QPushButton#loginSecondaryButton { background: #dbe7dd; color: #294638; }
            QPushButton#loginSecondaryButton:hover { background: #ceddD1; }
        """,
    },
    "DARK": {
        "label": "Dark Mode",
        "stylesheet": COMMON + """
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
            QPushButton#primary { background: #396fae; }
            QPushButton#danger { background: #9d4f55; }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit { background: #222833; color: #e6eaf0; border: 1px solid #3a424f; border-radius: 6px; padding: 6px; }
            QTableWidget, QListWidget { background: #1e232d; color: #e6eaf0; border: 1px solid #343c49; border-radius: 8px; alternate-background-color: #222833; }
            QHeaderView::section { background: #293241; color: #e6eaf0; padding: 8px; border: 0; font-weight: 700; }
            QGroupBox { background: #1e232d; border: 1px solid #343c49; border-radius: 9px; margin-top: 10px; padding: 12px 8px 8px; font-weight: 700; }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; background: #171a21; color: #cbd5e1; }
            QFrame#brandStrip { background: #293f5e; }
            QLabel#brandName, QLabel#brandVersion { color: #f4f7fb; }
            QLabel#cardTitle { color: #aab3c0; }
            QLabel#cardValue { color: #f4f7fb; }
            QFrame#card { background: #1e232d; border: 1px solid #343c49; }
            QLabel#total { background: #315f9f; color: white; }
            QTableWidget::item:selected { background: #334e70; color: #ffffff; }
            QFrame#loginCard { background: #1e232d; border: 1px solid #343c49; }
            QLabel#loginTitle { color: #f8fafc; }
            QLabel#loginVersion, QLabel#loginWelcome, QLabel#loginFieldLabel, QLabel#loginFooter { color: #aab3c0; }
            QPushButton#loginPrimaryButton { background: #396fae; color: #ffffff; }
            QPushButton#loginPrimaryButton:hover { background: #4b83c3; }
            QPushButton#loginSecondaryButton { background: #293241; color: #dbeafe; }
            QPushButton#loginSecondaryButton:hover { background: #344154; }
            QLineEdit#loginInput { background: #222833; color: #e6eaf0; border: 1px solid #3a424f; }
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
