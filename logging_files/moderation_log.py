#MIT License
#Copyright (c) 2020 Semih Aydın
#UTF-8

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")

file_handler = logging.FileHandler("./logs/moderation.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)