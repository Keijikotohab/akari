import glob
from Akari.engine.model import get_summary
class BertSum():
    def __init__(self):
        self.in_file = None
        self.out_summary = []

    def summarise(self,bakend='bert'):
        self.in_text = open(self.in_file,"r")
        for file in self.in_text:
            self.out_summaary.append(get_summary(file,bakend))

    def initialize(self):
        self.in_file = None
        self.out_summary = []

    def set_input(self,in_file,in_dir=None):
        self.in_file = in_file
        if in_dir == None:
            pass
        else:
            self.in_dir = in_dir
            self.in_dir = glob.glob(self.indir + '\\*.txt')


    def save(self,out_path):
        out_file = open(out_path,mode="w")
        out_file.write(out_summary[0])
        out_file.close()
