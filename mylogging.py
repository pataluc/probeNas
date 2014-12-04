#!/usr/bin/python
#   coding=UTF-8
#
#   Title: myLogging.py
#   Author: Luc Fouin <luc.fouin@gmail.com>
#   Date: 04/12/2014
#   Info: Define standard logger and logging properties
 
import __main__
import os
import logging
import logging.config


LOGGING_CONF = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'INFO'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.dirname(__main__.__file__) + '/logs/' + os.path.splitext(os.path.basename(__main__.__file__))[0] + '.log',
            'formatter': 'default',
            'level': 'DEBUG',
            'maxBytes': 10000000,
            'backupCount': 20
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file']
    }
}
               


# Chargement du fichier de conf logging
logging.config.dictConfig(LOGGING_CONF)


def getLogger(logger) :
    return logging.getLogger(logger)
