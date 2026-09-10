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
            QWidget { background: #fafafa; color: #262626; font-family: 'Segoe UI'; }
            QMainWindow, QDialog { background: #fafafa; }
            QMenuBar { background: #ffffff; color: #262626; border-bottom: 2px solid #d14343; }
            QMenuBar::item:selected, QMenu::item:selected { background: #fff1f1; color: #a51d1d; }
            QMenu { background: #ffffff; color: #262626; border: 1px solid #e5e5e5; }
            QTabWidget::pane { border: 0; background: #fafafa; }
            QTabBar { background: #fff5f5; }
            QTabBar::tab { background: #fff5f5; color: #7f1d1d; padding: 10px 16px; border: 0; }
            QTabBar::tab:selected { background: #ffffff; color: #b42323; border-bottom: 3px solid #d14343; }
            QPushButton { background: #c84a4a; color: white; border: 0; border-radius: 7px; padding: 8px 14px; font-weight: 700; }
            QPushButton:hover { background: #ad3939; }
            QPushButton#primary { background: #c43f3f; }
            QPushButton#danger { background: #9f2f2f; }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit { background: white; color: #262626; border: 1px solid #d6d6d6; border-radius: 6px; padding: 6px; }
            QTableWidget, QListWidget { background: white; color: #262626; border: 1px solid #e0e0e0; border-radius: 8px; alternate-background-color: #fffafa; }
            QHeaderView::section { background: #f8e5e5; color: #8f1d1d; padding: 8px; border: 0; font-weight: 700; }
            QGroupBox { background: white; border: 1px solid #e6d5d5; border-radius: 9px; margin-top: 10px; padding: 12px 8px 8px; font-weight: 700; }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; background: #fafafa; color: #a51d1d; }
            QFrame#brandStrip { background: #b93434; }
            QLabel#brandName, QLabel#brandVersion { color: white; }
            QLabel#cardTitle { color: #7b6262; }
            QLabel#cardValue { color: #5f2020; }
            QLabel#total { background: #a93232; color: white; }
            QFrame#loginCard { background: #ffffff; border: 1px solid #ead1d1; }
            QLabel#loginTitle { color: #7f1d1d; }
            QLabel#loginVersion, QLabel#loginWelcome, QLabel#loginFieldLabel, QLabel#loginFooter { color: #7f1d1d; }
            QPushButton#loginPrimaryButton { background: #c43f3f; color: #ffffff; }
            QPushButton#loginPrimaryButton:hover { background: #ad3939; }
            QPushButton#loginSecondaryButton { background: #fff1f1; color: #b71c1c; }
            QPushButton#loginSecondaryButton:hover { background: #ffe4e4; }
        """,
    },
    "KEAGAMAAN": {
        "label": "Keagamaan",
        "stylesheet": COMMON + """
            QWidget { background: #f5f7f4; color: #26382d; font-family: 'Segoe UI'; }
            QMainWindow, QDialog { background: #f5f7f4; }
            QMenuBar { background: #ffffff; color: #294638; border-bottom: 2px solid #6c8872; }
            QMenuBar::item:selected, QMenu::item:selected { background: #edf4ee; color: #315a40; }
            QMenu { background: #ffffff; color: #203027; border: 1px solid #d7e2d9; }
            QTabWidget::pane { border: 0; background: #f5f7f4; }
            QTabBar { background: #edf2ed; }
            QTabBar::tab { background: #edf2ed; color: #50675a; padding: 10px 16px; border: 0; }
            QTabBar::tab:selected { background: #ffffff; color: #315a40; border-bottom: 3px solid #66856f; }
            QPushButton { background: #62806a; color: white; border: 0; border-radius: 7px; padding: 8px 14px; font-weight: 600; }
            QPushButton:hover { background: #506d58; }
            QPushButton#primary { background: #587963; }
            QPushButton#danger { background: #9a5555; }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit { background: white; color: #203027; border: 1px solid #ccd8ce; border-radius: 6px; padding: 6px; }
            QTableWidget, QListWidget { background: white; color: #203027; border: 1px solid #d7e2d9; border-radius: 8px; alternate-background-color: #fafcf9; }
            QHeaderView::section { background: #e7efe9; color: #315a40; padding: 8px; border: 0; font-weight: 700; }
            QGroupBox { background: white; border: 1px solid #d7e2d9; border-radius: 9px; margin-top: 10px; padding: 12px 8px 8px; font-weight: 700; }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; background: #f5f7f4; color: #315a40; }
            QFrame#brandStrip { background: #5f7f68; }
            QLabel#brandName, QLabel#brandVersion { color: white; }
            QLabel#cardTitle { color: #65776b; }
            QLabel#cardValue { color: #294638; }
            QLabel#total { background: #506f59; color: white; }
            QFrame#loginCard { background: #ffffff; border: 1px solid #d7e2d9; }
            QLabel#loginTitle { color: #294638; }
            QLabel#loginVersion, QLabel#loginWelcome, QLabel#loginFieldLabel, QLabel#loginFooter { color: #50675a; }
            QPushButton#loginPrimaryButton { background: #587963; color: #ffffff; }
            QPushButton#loginPrimaryButton:hover { background: #476650; }
            QPushButton#loginSecondaryButton { background: #edf4ee; color: #315a40; }
            QPushButton#loginSecondaryButton:hover { background: #dfece1; }
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
