import numpy as np
import pandas as pd

from ..Enviroment_Variables import enviroment as env

from ..FileIO import GenomeData as gData
from ..FileIO import MetaData as mData

"""Wrapper for GenomeData and MetaData object as well as related processing"""
class DataService:
    metaData = mData.MetaData
    genomeData = gData.GenomeData
   

    # CONSTRUCTOR
    def __init__(self, genomeDataIn, metaDataIn):
        self.metaData = metaDataIn
        self.genomeData = genomeDataIn
        
    
    # SUBSCRIPTION
    # gets row of metadata given sequenceID
    def __getitem__(self, key):
        return self.metaData[key]
    
    
    # gets two sequences
    def get_sequence_pair(self, ID1,ID2):
        
        Sequence1=self.genomeData[ID1]
        Sequence2=self.genomeData[ID2]
        
        return (Sequence1, Sequence2)
    
    # gets multiple sequences
    def get_multiple_seqences(self,IdList):
        SequenceList = []
        for i in IdList:
            SequenceList.append(self.genomeData[i['sequence_id']])
        return SequenceList
    
    # returns a DF of all present PLZ
    def get_all_PLZ(self):
        return self.metaData.getAllPostalCodes()
    
    

    # returns a DF of all PLZ formatted for display in table
    def get_all_PLZ_DataTable(self):
        DF = self.metaData.getAllPostalCodes()

        DF=DF.dropna()
        
        # inserts selected column for table
        DF.insert(0, "selected", np.full(len(DF[env.META_POSTAL]), False))                
        
        # renames columns to ts equivalent
        DF=DF.rename(columns={"selected":"selected", env.META_POSTAL:"postal_code"}, errors="raise")
        
        return DF
    
    # returns all present pangolin lineages
    def get_all_pangolin_lineages(self):
        return self.metaData.getUniquePangolinLineages().dropna()
        
    
    # returns DF of sequences at given plz, trimmed for relevance to UI
    def get_all_seq_in_PLZ(self,plz):
        
        DF = self.get_all_in_plz(plz)
        
        # filters DF to rows that contain given plz
        DF = DF[DF[env.META_POSTAL] == plz]
        result = pd.DataFrame(columns = ['Sequence_id','Sequence'])
        
        # remaps index to sequence ID
        for i in DF.index:
            result.loc[i] = [i,self.genomeData[i]]
        
        return result
    
    # returns DF of sequences at given plz including ALL metadata
    def get_all_seq_attributes_in_PLZ(self,PLZ):
        return self.metaData.getInPostalCode(PLZ)
    
    # returns DF of sequences including metadata  
    def get_all_seq_table_values_in_PLZ(self,PLZ):

        left = self.get_all_seq_in_PLZ(PLZ)

        right = self.get_all_seq_attributes_in_PLZ(PLZ)

        
        return pd.merge(left, right, left_index = True, right_index = True)
    
    # returns DF of all metadata in a given PLZ
    def get_all_in_plz(self, plz):
        return self.metaData.getInPostalCode(plz)

    # puts sequences in Muscle FASTA file and returns file path
    def get_Muscle_Fasta_File(self, Sequences):
        
        with open(env.MUSCLE_IN_FILE_PATH, 'w') as f:
            
            for i in Sequences:
                seq = self.genomeData[i]
                f.write('>' + i + "\n")
                f.write(seq + " \n")
                
        return env.MUSCLE_IN_FILE_PATH
        

from ..FileIO.GenomeData import gendata
from ..FileIO.MetaData import geodata
dataService = DataService(gendata,geodata)
 
