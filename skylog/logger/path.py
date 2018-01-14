import os
import logging
import threading
from queue import Queue
# import multiprocessing

import inotify
from inotify import adapters
from skylog.exceptions.error import random_error

log = '%(asctime)s %(levelname)s:%(message)s'
logging.basicConfig(format=log, level=logging.DEBUG)


class WatchDog:
    """Watch files and directories for changes
    """

    def __init__(self, path):
        """Initialize WatchDog class

        :param path: string
        """
        self.path = path
        self.paths = Queue()
        self.threads = Queue()
        self.running = Queue()
        self.watching = Queue()

        # Ensure string
        try:
            test = self.path.encode('utf8')
        except AttributeError as e:
            self.path = self.path.decode()
            logging.exception(str(e))

        # Ensure path is a directory
        try:
            if os.path.isdir(self.path):
                logging.debug('Path exists {}'.format(self.path))
        except OSError as e:
            logging.exception(str(e))
            logging.exception(random_error())
            raise

        # Create a list of executable directories
        top = self.path
        walk = os.walk(top)
        allowed = os.X_OK
        for directory, _, _ in walk:
            if os.access(directory, allowed):
                self.paths.put(directory)
                logging.debug('Queueing {}'.format(directory))

    def start(self):
        """Start WatchDog threads

        :return: tuple (watch_path, filename)
        """

        # TODO: add multiprocessing to get around GIL
        # TODO: do I need to add a lock?
        # TODO: threading does not work

        def worker_thread(path):
            try:
                watch = inotify.adapters.Inotify()
                watch.add_watch(path)
                logging.debug('{} created'.format(watch))
            except Exception as e:
                logging.exception(str(e))

                # try:
                #     for event in watch.event_gen():
                #         if event is not None:
                #             (header, type_names, watch_path, filename) = event
                #             self.watching.put(event)
                #             logging.debug((header, type_names, watch_path, filename))
                #
                # except Exception as e:
                #     logging.exception(str(e))

        def create_thread(path):
            thread = threading.Thread(target=worker_thread(path))
            logging.debug('Created thread {}'.format(thread.name))
            return thread

        def start_thread(thread):
            thread.daemon = True
            logging.debug('Started thread {}'.format(thread.name))
            return thread.start()

        while self.paths.empty() is not True:
            path = self.paths.get()
            thread = create_thread(path)
            self.threads.put(thread)

        while self.threads.empty() is not True:
            thread = self.threads.get()
            running = start_thread(thread)
            self.running.put(running)

    def stop(self):
        """Stop WatchDog threads

        :return: boolean
        """
        # TODO: fix reference queue to self.running
        while self.running.empty() is not True:
            thread = self.running.get()
            thread.alive = False
            thread.join()
            logging.debug('Thread stopped {}'.format(thread))
