class LoggerInstance(object):
    def __new__(cls):
        from common.utility.logger.custom_logging import LogHandler
        return LogHandler()


# instance creation
logger_instance = LoggerInstance()
