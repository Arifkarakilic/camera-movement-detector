from utils.time_utils import current_timestamp

def log_event(message, logfile="logs/system.log"):
    """
    Args:
        message (str): Yazılacak mesaj
        logfile (str): Hedef log dosyası (varsayılan: logs/system.log)
    """
    from os import makedirs
    from os.path import dirname, exists

    log_dir = dirname(logfile)
    if not exists(log_dir):
        makedirs(log_dir)

    with open(logfile, "a", encoding="utf-8") as f:
        f.write(f"[{current_timestamp()}] {message}\n")
