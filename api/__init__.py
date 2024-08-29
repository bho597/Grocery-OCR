# import logging
# import sys


# logger = logging.getLogger(__name__)

# fh = logging.FileHandler('job_logger.log')
# fh.setLevel(logging.DEBUG)


# def setup_logging():
#     msg_format = '%(asctime)s [%(levelname)8s] %(message)s (%(name)s - %(filename)s:%(lineno)s)'
#     date_format = '%Y-%m-%d %H:%M:%S'
#     formatter = logging.Formatter(fmt=msg_format, datefmt=date_format)
#     console_handler = logging.StreamHandler(stream=sys.stdout)
#     console_handler.setLevel(logging.DEBUG)
#     console_handler.setFormatter(formatter)
#     logger.addHandler(console_handler)
#     logger.setLevel(logging.DEBUG)
#     logger.propagate = False