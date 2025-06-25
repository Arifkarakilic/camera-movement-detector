from datetime import datetime

def current_timestamp(fmt="%Y-%m-%d %H:%M:%S"):
    """

    Args:
        fmt (str): Zaman formatı (default: '%Y-%m-%d %H:%M:%S')

    Returns:
        str: Formatlı zaman damgası
    """
    return datetime.now().strftime(fmt)
