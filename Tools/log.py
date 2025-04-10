from datetime import datetime


class Logger:
    """日志记录类，用于记录软件使用过程中的各个信息"""
    def __call__(self,msg,time_stamp=None):
        self.msg=msg
        self.time_stamp=time_stamp
        if  self.time_stamp is None:
            self.time_stamp= datetime.now()
        return self.time_stamp.strftime("[%Y-%m-%d-%H:%M:%S]")+self.msg



