import datetime
# 源文件
class File_issues:
    def __init__(self, file):
        self.commit = file[1]
        if file[6] == 0:
            self.filePath = file[4]
            self.new_filePath = file[3]
        elif file[6] == 1:
            self.new_filePath = file[4]
            self.filePath = file[3]
        self.addedLine = file[7]
        self.removedLine = file[8]
        self.committed_date = datetime.datetime.strptime(file[2].replace("T", " ").replace("Z", "")[:19], "%Y-%m-%d %H:%M:%S")