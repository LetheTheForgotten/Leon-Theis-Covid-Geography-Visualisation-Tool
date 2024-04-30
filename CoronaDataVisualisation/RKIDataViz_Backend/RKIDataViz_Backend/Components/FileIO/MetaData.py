from datetime import datetime
import pandas
from ..Enviroment_Variables import enviroment as env
"""Wrapper for Parsed Meta-data"""

class MetaData:
    
    data = pandas.DataFrame
    
    # CONSTRUCTOR
    # forces postal codes to be strings, forces dates to be in datetime format, sets sequenceID as dataframe index
    def __init__ (self, path):
        print("Parsing Meta-data TSV...")
        
        self.data = pandas.read_csv(path,sep = '\t',dtype = {env.META_POSTAL:str}) 
        self.data[env.META_SEQUENCE_DATE] = pandas.to_datetime(self.data[env.META_SEQUENCE_DATE], format = "%Y-%m-%d")
        self.data.set_index(env.META_SEQUENCE_ID,inplace = True)
        
        print("Meta-data Finished!")
    
    # Getter for MetaData dataframe
    def getData(self):
        return self.data
    
    # SUBSCRIPTION
    # get a row of the meta-data given a sequenceID
    def __getitem__(self, key):
        # error raised if key is not string
        if not isinstance(key,str):
            raise ValueError("key must be a string")
        
        return self.data.loc[key]
    
   
    # get all sequences sampled in given postal code
    def getInPostalCode(self, plz):
        
        # PLZ raises error if not string
        if not isinstance(plz,str):
            raise ValueError("getInPostalCode requires string as input")
        
        return pandas.DataFrame(self.data.loc[self.data[env.META_POSTAL] == plz])
    
    
    # get all sequences sampled in given postal code in given date range
    def getInPostalCodeInDateRange(self, plz, start, end):
        
        #PLZ raises error if not string
        if not isinstance(plz, str):
            raise ValueError("getInPostalCode requires string as input")
        
        DF = self.data.loc[self.data[env.META_SEQUENCE_DATE] >= start]
        DF = DF.loc[DF[env.META_SEQUENCE_DATE] <= end]
        DF = DF.loc[DF[env.META_POSTAL] == plz]
        
        return DF 
        
    # returns dataframe of every unique PLZ in the meta-data
    def getAllPostalCodes(self):
        
        DF = self.data[[env.META_POSTAL]].drop_duplicates()

        DF = DF.reset_index(drop=True)
        return DF
    
    def getUniquePangolinLineages(self):
        DF = self.data[[env.META_PANGOLIN]].drop_duplicates()
        DF = DF.reset_index(drop = True)
        
        return DF
    
geodata = MetaData(env.METADATA_FILE)