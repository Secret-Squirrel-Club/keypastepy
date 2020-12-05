#!/usr/bin/env python3

import logging

class KeyPasteException(Exception):
    pass

class BaseKeyClass(object):
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def debug(self, message: str):
        return self.logger.DEBUG(message)    
    
    def info(self, message: str):
        return self.logger.info(message)
    
    def error(self, message: str):
        return self.logger.error(message)

    def warn(self, message: str):
        return self.logger.warning(message) 
    
    def critical(self, message: str):
        return self.logger.critical(message)

    def exception(self, message: str):
        return self.logger.exception(message)
