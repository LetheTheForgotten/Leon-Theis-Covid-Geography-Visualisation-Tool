import mmap
from concurrent.futures import ThreadPoolExecutor
import queue
import os
import pandas
import json
from ..Enviroment_Variables import enviroment as env


"""Inteface that preforms read and write operations on given sequence file"""
class FileReader:
    AddressTable = dict()
    MemFile = None
    
    # CONSTRUCTOR
    # Constructor can get a fasta file and a function to parse it or a fasta file and an address JSON file
    def __init__ (self, path, funct, JSON = ""):
        
        # checks if parsing function or JSON was given as second constructor argument
        if JSON!="":
            print("\nFilling GenomeData address dictionary using " + JSON +" \n")
            # imports json and translates to dictionary
            with open(JSON) as  jsonFile:
                data = json.load(jsonFile)
                self.AddressTable.update(data)
            jsonFile.close
            self.openmmap(path)
        
        # else parse given file using multi-threaded methodology
        else:
            print("\nGenerating GenomeData address dictonary \n")
            self.AddressTable.update(self.parse_fasta_multithreaded(path,funct))    
            self.openmmap(path)

    # SUBSCRIPTION
    # returns genome sequence of given sequence ID
    def __getitem__(self, index):
            # slice operations (function[1:2]) cause crashes, raise exception if noticed    
            if isinstance(index, slice):
                raise Exception("slicing does not work")

            address = self.AddressTable[index]
            return self.MemFile[address[0]:address[1]].decode("utf-8")


    # Export address dictionary as JSON file
    def export_Json(self, JsonPath):
        print("\nexporting address dictionary to JSON...")
        
        with open(JsonPath,"w") as outfile:
            json.dump(self.AddressTable,outfile)
            
        outfile.close
        print("\njson file of address dictionary generated at "+ JsonPath +"\n")
        
    # opens mmap that address dictionary is relative to
    def openmmap(self, path):
        
        with open(path, "r+b") as fh:
            self.MemFile = mmap.mmap(fh.fileno(),0)

    # closes said mmap file
    def closemmap(self):
        
        self.MemFile.close()
    
    # getter for address of a given sequenceID
    def getAddr(self, key):
        return self.AddressTable[key]

    # corrects a given address range to contain the start and end of a line
    def correct_chunk_end(self, file, end, maxIndex):
    
        mm = file
    
        endChar = ''
        endCharIndex = end
        
        while(endChar != env.HEADER_CHAR and endCharIndex < maxIndex):
            endChar = mm[endCharIndex]
            endCharIndex += 1
    
        if endCharIndex == maxIndex:
            return endCharIndex
    
        return endCharIndex - 1

    # returns n address ranges that will contain complete lines per correct_chunk_end
    def find_chunks(self, file, threadNums):
        
        with open(file, "r+b") as fh:
            
            mm = mmap.mmap(fh.fileno(),0)
        
            endIndex = os.path.getsize(file)
        
            interval = int(endIndex/threadNums)
        
            chunks = list()
            chunkEnd = 0
            
            for i in range(1, threadNums + 1):
                
                # correct chunk start and end
                corrected_chunk=self.correct_chunk_end(mm, interval * i, endIndex - 1)
                
                # add found chunk to list
                chunks.append((chunkEnd, corrected_chunk - 1))
                
                # set next start
                chunkEnd = corrected_chunk
                

            mm.close
            fh.close
        return chunks

    # multithreaded function to fill dictionary with addresses of lines
    def seed_Dict_Multithread(self, file, start, end, queue, threadNum, function):
        print("Starting Thread %s, Range: %s to %s \n"%(threadNum, start, end))
        
        with open(file, "r+b") as fh:
            interimDict = dict()
            start = int(start[0])
            end = int(end[0])
        
            mm = mmap.mmap(fh.fileno(), 0)
        
            function(interimDict, mm, start, end)
            
            queue.put(interimDict)
            mm.close()
            
        fh.close()
    
        print("Thread %s Finished \n"%(threadNum))
    
   
    #instantiates threads for parsing given sequence file
    def parse_fasta_multithreaded(self, fname, function):
        
        threadNums = env.THREAD_COUNT
        
        print("FASTA parsing Started...")
        
        myqueue = queue.Queue()
        chunkList = self.find_chunks(fname, threadNums)
        interimDict = dict()
        namelist = list()
        Qlist = list()
        threadNum = list()
        functlist = list()
    
        for i in range(0, threadNums):
        
            namelist.append(fname)
            Qlist.append(myqueue)
            threadNum.append(i)
            functlist.append(function)
        
        # seperates sets into columns that can be parsed properly
        MemDF = pandas.DataFrame(chunkList, columns = ["start", "end"])
    
        print("Executor Starting")
    
        with ThreadPoolExecutor(max_workers = threadNums) as executor:      
            result = executor.map(
                        self.seed_Dict_Multithread, 
                        namelist, 
                        MemDF.filter(items = ["start"]).values, 
                        MemDF.filter(items = ["end"]).values, 
                        Qlist, 
                        threadNum, 
                        functlist
                      )
            
            # update global address dictionary with results of thread from queue
            for res in result:
                interimDict.update(myqueue.get())
           
        print("parsing finished \n \n")
        return interimDict
    


