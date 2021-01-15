#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/2/25
# @Author  : Mcen (mmocheng@163.com)
# @Name    : log_conf
# coding=utf-8
"""
定义执行日志
"""



import logging,time,os
from Common.ElementPath import Element


def loggering(name = __name__):
    logger = logging.getLogger('')
    logger.setLevel(level=logging.INFO)
    log_date = time.strftime("%Y-%m-%d")
    log_file = log_date + '_run_logging.log'
    if not os.path.exists(Element.LOGS):
        os.mkdir(Element.LOGS)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M',
                        filename=Element.LOGS + "/"  + log_file,
                        # filename='../../OutPuts/logs/' + log_file,
                        filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    console.setFormatter(formatter)
    
    logger.addHandler(console)


def setup_log(name=__name__):
        logger = logging.Logger(name)
        logger.setLevel(logging.DEBUG)

        log_date = time.strftime("%Y-%m-%d")
        log_file = log_date + '_run_logging.log'
        if not os.path.exists(Element.LOGS):
            os.mkdir(Element.LOGS)
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setLevel(logging.INFO)

        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)

        logger.addHandler(sh)
        logger.addHandler(fh)
        

if __name__ == '__main__':
    loggering()
    logging.debug('debug message')
    logging.info('info message')
    logging.warning('warning message')
    logging.error('error message')
    logging.critical('critical error message')
