import logging


# FORMATSTRING = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
# FORMATSTRING = "%(levelname)s - [%(asctime)s] - {M:%(module)s/F:%(funcName)s/L:%(lineno)04d} -\n>>> %(message)s"

# FORMATSTRING = "%(levelname)s/%(asctime)s - %(message)s"
FORMATSTRING = "%(levelname)8s | %(message)s"
DATEFORMAT = 'D:%Y%m%d/%Z:%H%M%S'

logging.basicConfig(
    level=logging.INFO,
    format=FORMATSTRING,
    datefmt=DATEFORMAT
)

logger = logging.getLogger(name="TC-log")
# logger = logging.getLogger(name=LOGGER_NAME)

