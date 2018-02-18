
import timeit


def decorator_elapsed_timer(func):
    """decorator function"""
    def new_func(*args, **kwargs):
        start = timeit.default_timer()
        ret = func(*args, **kwargs)
        elapsed = (timeit.default_timer() - start)
        print('Elapsed time: %s' % elapsed)
        return ret
    return new_func


class ElapsedTimer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self._start()
        return self

    def __exit__(self, *args):
        self._end()
        if self.verbose:
            self.print_elapsed()

    def _start(self):
        self.start = timeit.default_timer()

    def _end(self):
        self.end = timeit.default_timer()
        self.secs = self.end - self.start

    def print_elapsed(self):
        if not hasattr(self, 'secs'):
            self._end()
        print('Elapsed time: %f seconds' % (self.secs))
