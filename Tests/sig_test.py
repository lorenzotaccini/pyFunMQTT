import sys
import time
import signal


def _handle_signal(*args, **kwargs):
    print('Signal handler has been called.')
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, _handle_signal)

    while True:
        time.sleep(1)
