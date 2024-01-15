class File_tracescore:
    def __init__(self, file):
        self.commit = file[1]
        # self.filePath = file[1]
        # self.addedLine = file[2]
        # self.removedLine = file[3]
        self.committed_date = file[3]
        self.new_filePath = file[2]
