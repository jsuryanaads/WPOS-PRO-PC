from ..models import Setting

DEFAULT_SETTINGS = {
    "store_name": "TOKO SEMBAKO",
    "store_address": "",
    "store_phone": "",
    "receipt_footer": "Terima kasih sudah berbelanja",
    "receipt_paper": "80mm",
    "printer_name": "",
}


def get_setting(session, key, default=""):
    row = session.query(Setting).filter_by(key=key).first()
    return row.value if row else default


def get_settings(session):
    return {key: get_setting(session, key, default) for key, default in DEFAULT_SETTINGS.items()}


def set_setting(session, key, value):
    key = str(key).strip()
    if not key:
        raise ValueError("Key pengaturan wajib diisi")
    row = session.query(Setting).filter_by(key=key).first()
    if row:
        row.value = str(value)
    else:
        row = Setting(key=key, value=str(value))
        session.add(row)
    session.commit()
    session.refresh(row)
    return row


def save_settings(session, values):
    """Save a group of settings in one atomic transaction."""
    try:
        for key, value in values.items():
            key = str(key).strip()
            if not key:
                raise ValueError("Key pengaturan wajib diisi")
            row = session.query(Setting).filter_by(key=key).first()
            if row:
                row.value = str(value)
            else:
                session.add(Setting(key=key, value=str(value)))
        session.commit()
    except Exception:
        session.rollback()
        raise
