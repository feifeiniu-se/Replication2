import datetime
class Commit:
    def __init__(self, info):
        self.hash = info[0]
        #使用bug报告提交时间
        self.commit_date = datetime.datetime.strptime(info[1].replace("T", " ").replace("Z", ""), "%Y-%m-%d %H:%M:%S")
        self.message = info[2]
        self.files = set()