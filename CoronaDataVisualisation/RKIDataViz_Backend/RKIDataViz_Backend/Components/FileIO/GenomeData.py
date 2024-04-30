from . import FileReader as Reader
from ..Enviroment_Variables import enviroment as env


"""Wrapper Object for Parsed FASTA File"""


##Function Pointer
##Parses given mmap file from given start to given end address and puts into dictionary 
##REQUIREMENTS:
##function must accept a dictionary, a mmap file, the start and end address of the chunk it is parsing
##function MUST put resulting memory pointers into the dictionary it was given
def parse(tempDict, mm, start, end):    
        
            mm.seek(start)            

            identifier = None
            line = mm.readline()
            line = line.strip()

            while(line != None):

                if line.startswith(b'>'):
                    identifier = line

                else:

                    tempDict[identifier.decode("utf-8")[1:]] = (position,mm.tell())
                    identifier = line
                if(not mm.tell() <= end):
                     break
                
                position = mm.tell()
                line = mm.readline()
                line = line.strip()


#the reader object   
data = Reader.FileReader
            

class GenomeData:   

    #CONSTRUCTOR      
    #JSON defaults to none to make constructor variable
    def __init__ (self, path, JSON = env.FILEREADER_JSON_PATH_READ):
        print("Creating GenomeData Object")
        self.data = Reader.FileReader(path, parse, JSON) 
        if(env.FILEREADER_JSON_PATH_READ==""):
            self.getJSON(env.FILEREADER_JSON_PATH_OUT)

    #Getter for FileReader Object
    def getData(self):
        return self.data
    
    #get entry in address dictionary
    def getAddress(self, key):
        return self.data.getAddr(key)

    #SUBSCRIPTION
    #gets sequence given key
    def __getitem__(self, index):
        #strings end with /n/r, slicing here rather than in filereader to prevent issues
        return self.data[index][:-4]
    
    #outputs JSON file representing current address dictionary
    def getJSON(self, JsonPath):
        self.data.export_Json(JsonPath)
       

gendata=GenomeData(env.FASTA_FILE)