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

    # Crea un handler per lo stdout
    console_handler = logging.StreamHandler(stream=sys.stdout)
    if verbose:
        console_handler.setLevel(logging.DEBUG)
    else:
        console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    # Crea un handler per il file di log con rotazione
    file_handler = RotatingFileHandler(
        'app.log', maxBytes=5 * 1024 * 1024, backupCount=3
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Aggiungi gli handler al logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


if __name__ == '__main__':
    run_args = cli.CLI()
    setup_logger(run_args.args.verbose)

    client_spawner = core.Spawner(run_args)
    client_spawner.spawn_all()
    while True:
        if input() == 'q':
            client_spawner.shutdown()
