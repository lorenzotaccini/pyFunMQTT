import os

import Worker.core as core
import Utils.cli as cli

import logging
import sys
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


def setup_logger(verbose, silent, logmessages):
    logger = logging.getLogger()

    '''
    # add level MESSAGE to the logger, his numeric value will be 5, the lowest
    msg_log_lvl = 5
    
    def message(self, msg, *args, **kws):
        if self.isEnabledFor(msg_log_lvl):
            self._log(msg_log_lvl, msg, args, **kws)

    logging.addLevelName(msg_log_lvl, "MESSAGE")
    logging.Logger.message = message
    '''

    logger.setLevel(logging.DEBUG)  # setup logging level

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s: %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S'
    )

    '''
    if logmessages:
        # create a handler for logging messages, with rotation and dimension for each file capped to 3MB
        msgs_file_handler = RotatingFileHandler(
            (os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Logs', 'msgs.log')),
            maxBytes=3 * 1024 * 1024,
            backupCount=3
        )
        msgs_file_handler.setLevel(logging.MESSAGE)
        msgs_file_handler.addFilter(lambda record: record.levelno < logging.DEBUG)  # only log MESSAGE
        msgs_file_handler.setFormatter(formatter)
        logger.addHandler(msgs_file_handler)
    '''

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
