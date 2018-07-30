import os
from os import listdir
from os.path import isfile, join


class RotatingFile():
    def __init__(self, filepath="/var/log/picontroller/log"):
        self.path = filepath
        self.log_dir = os.path.dirname(self.path)
        self.file_name = os.path.basename(self.path)
        self.maxsize=1000000


    def log(self, msg):
        try:
            with open(self.path, 'a') as f:
                f.write("{log}\n".format(log=msg))
        except IOError as e:
            print str(e)
            print "Error writing to temp file {f}".format(self.path)
        self.check_rotate()


    def check_rotate(self):
        statinfo = os.stat(self.path)
        if statinfo.st_size > self.maxsize:
            self.rotate_files()

    def rotate_files(self):
        # Remove 20
        oldf = os.path.join(self.log_dir, self.file_name + "20")
        if os.path.isfile(oldf):
            os.remove(oldf)

        n = 20
        while n > 0:
            oldf = os.path.join(self.log_dir, self.file_name + str(n))
            newf = os.path.join(self.log_dir, self.file_name + str(n+1))
            if os.path.isfile(oldf):
                os.rename(oldf, newf)
            n = n - 1

        oldf = os.path.join(self.log_dir, self.file_name,)
        newf = os.path.join(self.log_dir, self.file_name + "1")
        if os.path.isfile(oldf):
            os.rename(oldf, newf)
        os.system("touch " + self.path)
