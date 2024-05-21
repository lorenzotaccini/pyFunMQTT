import Worker.core as core
import Utils.cli as cli

import logging
import sys
from logging.handlers import RotatingFileHandler


def setup_logger(verbose):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # setup logging level

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s: %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S'
    )

    # all messages below WARNING level are logged on stdout
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.addFilter(lambda record: record.levelno < logging.WARNING)

    # all messages beyond INFO level are logged on stderr
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)

    # Crea un handler per il file di log con rotazione
    file_handler = RotatingFileHandler(
        'app.log', maxBytes=5 * 1024 * 1024, backupCount=3
    )

    if verbose:
        stdout_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.DEBUG)
    else:
        stdout_handler.setLevel(logging.WARNING)
        file_handler.setLevel(logging.WARNING)

    file_handler.setFormatter(formatter)
    stdout_handler.setFormatter(formatter)
    stderr_handler.setFormatter(formatter)

    # Aggiungi gli handler al logger
    logger.addHandler(stdout_handler)
    logger.addHandler(file_handler)
    logger.addHandler(stderr_handler)


if __name__ == '__main__':
    run_args = cli.CLI()
    setup_logger(run_args.args.verbose)

    client_spawner = core.Spawner(run_args)
    client_spawner.spawn_all()
    while True:
        if input().lower() == 'q':
            client_spawner.shutdown()
