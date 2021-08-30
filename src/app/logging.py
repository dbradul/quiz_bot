import logging

log_file = "./logfile.log"
log_level = logging.INFO #DEBUG
logging.basicConfig(level=log_level, filename=log_file, filemode="w+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")
logger = logging.getLogger("quiz_bot")


def entering(func):
    """ Pre function logging """
    logger.debug("Entered %s", func.__name__)


def exiting(func):
    """ Post function logging """
    logger.debug("Exited  %s", func.__name__)


# def log(func=None, *, pre=entering, post=exiting):
#     if func is not None:
#         return lambda func: log(func, pre=entering, post=exiting)

def log(pre=entering, post=exiting):

    """ Wrapper """
    def decorate(func):
        """ Decorator """
        def call(*args, **kwargs):
            """ Actual wrapping """
            pre(func)
            result = func(*args, **kwargs)
            post(func)
            return result
        return call
    return decorate
