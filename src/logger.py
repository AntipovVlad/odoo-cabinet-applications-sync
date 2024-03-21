import logging

log = logging.getLogger()
log.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")

full_log = logging.FileHandler("logs/work.log", "a", "utf-8")
full_log.setLevel(logging.INFO)
full_log.setFormatter(formatter)
log.addHandler(full_log)

error_log = logging.FileHandler("logs/errors.log", "a", "utf-8")
error_log.setLevel(logging.WARNING)
error_log.setFormatter(formatter)
log.addHandler(error_log)
