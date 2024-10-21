import os

import Worker.core as core
import Utils.cli as cli

import logging
import sys
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


def setup_logger(verbose, silent, logmessages):
    logger = logging.getLogger()


    logger.setLevel(logging.DEBUG)  # setup logging level

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s: %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S'
    )


    if not silent:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        if verbose:
            stdout_handler.setLevel(logging.INFO)
        else:
            stdout_handler.setLevel(logging.WARNING)
        logger.addHandler(stdout_handler)

    if logmessages:
        logfile_handler = TimedRotatingFileHandler(
            (os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Logs', 'session.log')),
            when='M',
            interval=1,  # new file everyday
            backupCount=7  # keeps the backups for a week before rollover
        )
        logfile_handler.suffix = '%d_%m_%Y'
        logfile_handler.setFormatter(formatter)
        logger.addHandler(logfile_handler)


if __name__ == '__main__':
    run_args = cli.CLI()
    setup_logger(run_args.args.verbose, run_args.args.silent, run_args.args.log_messages)

    client_spawner = core.Spawner(run_args)
    client_spawner.spawn_all()
    while True:
        if input().lower() == 'q':
            client_spawner.shutdown()
