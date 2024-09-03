import atexit
import logging
import logging.handlers
import queue
import sys

from pythonjsonlogger import jsonlogger


logger = logging.getLogger("gamedriver")


def _setup_logging() -> None:
    formatter = jsonlogger.JsonFormatter("%(levelname)s %(message)s")
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    # TODO: Get log path and enable file logging
    # file_handler = logging.handlers.RotatingFileHandler(
    #     "log.jsonl", maxBytes=10 * 1024 * 1024, backupCount=2
    # )
    # file_handler.setFormatter(formatter)

    # # Use a queue for the non-critical file logging so it doesn't block.
    # # See https://docs.python.org/3/howto/logging-cookbook.html#dealing-with-handlers-that-block
    # q = queue.Queue(-1)  # no limit on size
    # queue_handler = logging.handlers.QueueHandler(q)
    # queue_listener = logging.handlers.QueueListener(
    #     q, file_handler, respect_handler_level=True
    # )
    # queue_listener.start()
    # atexit.register(queue_listener.stop)

    logging.basicConfig(
        # encoding="utf-8", handlers=[stdout_handler, queue_handler]
        encoding="utf-8",
        handlers=[stdout_handler],
    )
