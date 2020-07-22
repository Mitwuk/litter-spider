# -*-coding:utf-8-*-
# @time: 2020/5/3 11:12
# @author: Mitwuk
# @description: 日志工具类

import logging
import logging.handlers
import time

import settings
import sys


class LogHelper(object):
    def __init__(self, log_name=None):
        """
        初始化
        :param log_name: 文件名
        :return:
        """
        if log_name is None:
            raise ValueError('log name is none')
        self.LOG_NAME = log_name

    def get_logger(self):
        dt = time.strftime("%Y-%m-%d", time.localtime())
        log_file_info = '%s/%s/info_%s.log' % (settings.PROJECT_ROOT_PATH, settings.LOG_FILE_INFO, dt)
        log_file_error = '%s/%s/error_%s.log' % (settings.PROJECT_ROOT_PATH, settings.LOG_FILE_ERROR, dt)
        log_handler_info = logging.handlers.RotatingFileHandler(log_file_info, maxBytes=1024 * 1024 * 10,
                                                                backupCount=10)
        log_handler_err = logging.handlers.RotatingFileHandler(log_file_error, maxBytes=1024 * 1024 * 10,
                                                               backupCount=10)
        fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
        # 实例化formatter
        formatter = logging.Formatter(fmt)

        # 设置过滤等级
        info_filter = logging.Filter()
        info_filter.filter = lambda record: record.levelno < logging.WARNING
        err_filter = logging.Filter()
        err_filter.filter = lambda record: record.levelno >= logging.WARNING
        log_handler_info.addFilter(info_filter)
        log_handler_err.addFilter(err_filter)
        # 控制台打印
        console = logging.StreamHandler(sys.stderr)
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        # 为handler添加formatter
        log_handler_info.setFormatter(formatter)
        log_handler_err.setFormatter(formatter)
        logger = logging.getLogger(self.LOG_NAME)
        # 为logger添加handler
        logger.addHandler(console)
        logger.addHandler(log_handler_info)
        logger.addHandler(log_handler_err)
        logger.setLevel(logging.INFO)
        return logger
