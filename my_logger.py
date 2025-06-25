import logging
import time
import os

class MyLogger():
    def __init__(self):
        #定义一个记录器
        self.logger = logging.getLogger('my_logger')
        #设置记录器日志级别
        self.logger.setLevel(logging.DEBUG)

        #定义一个控制台输出的处理器
        console_handler = logging.StreamHandler()
        #设置控制台输出的日志级别
        console_handler.setLevel(logging.WARNING)


        file_name = time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'


        #获取当前文件目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        current_path = os.path.join(current_dir,'logs', file_name)
        if not os.path.exists(current_path):
            os.makedirs(os.path.join(current_dir, 'logs'),exist_ok=True)

        #定义一个文件输出的处理器
        file_handler = logging.FileHandler(filename=current_path, encoding='utf-8')
        #设置文件输出的日志级别
        file_handler.setLevel(logging.INFO)

        #设置日志格式:    时间戳，文件名 - %(filename)s，日志级别，行号，日志信息
        formatter = logging.Formatter('%(asctime)s - %(levelname)s -%(lineno)d - %(message)s')
        #设置处理器的日志格式
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        #将处理器添加到记录器中
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

if __name__ == '__main__':
    my_logger = MyLogger().logger

    my_logger.debug('This is a debug message')
    my_logger.info('This is an info message')
    my_logger.warning('This is a warning message')


        
