from PySide6.QtWidgets import QPushButton, QGroupBox, QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTableWidget


def _polish_page(window, index, object_name, table_min_height=220):
    page = window.tabs.widget(index)
    if page is None:
        return
    page.setObjectName(object_name)
    page.setStyleSheet(f'''
        QWidget#{object_name} QGroupBox {{
            margin-top: 12px;
            padding-top: 18px;
            font-weight: 700;
        }}
        QWidget#{object_name} QLineEdit,
        QWidget#{object_name} QComboBox,
        QWidget#{object_name} QSpinBox,
        QWidget#{object_name} QDoubleSpinBox {{
            min-height: 36px;
        }}
        QWidget#{object_name} QTableWidget {{
            min-height: {table_min_height}px;
        }}
    ''')
    for button in page.findChildren(QPushButton):
        text = button.text().strip().lower()
        if any(key in text for key in ('hapus', 'delete', 'restore', 'nonaktif', 'reset')):
            button.setObjectName('danger')
        elif any(key in text for key in ('simpan', 'save', 'backup', 'cetak', 'print', 'pilih file')):
            button.setObjectName('primary')


def apply_system_ux(window):
    if not hasattr(window, 'tabs'):
        return
    _polish_page(window, 7, 'settingsPage', 180)
    _polish_page(window, 8, 'printerPage', 180)
    _polish_page(window, 9, 'backupPage', 220)
