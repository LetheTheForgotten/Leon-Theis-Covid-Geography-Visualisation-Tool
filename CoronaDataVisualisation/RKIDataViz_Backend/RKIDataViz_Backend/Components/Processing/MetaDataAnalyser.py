"""wrapper for functions doing analysis on stats that come primarily from the meta-data"""

import numpy as np
from pandas import DataFrame
from .DataService import dataService as dataService
from ..Enviroment_Variables import enviroment as env
"""pangolin lineage based calculations and the like"""

def sorensen_dice_coefficent_self_diff_dates(PLZ,start1,end1, start2, end2, minCount):
        # https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient
    DF1 = dataService.get_all_in_plz(PLZ)
    DF1 = DF1[(DF1[env.META_SEQUENCE_DATE] >= start1) & (DF1[env.META_SEQUENCE_DATE] <= end1)]
    DF2 = dataService.get_all_in_plz(PLZ)
    DF2 = DF2[(DF2[env.META_SEQUENCE_DATE] >= start2) & (DF2[env.META_SEQUENCE_DATE] <= end2)]
    if len(DF1[env.META_SEQUENCE_DATE]) < minCount or len(DF2[env.META_SEQUENCE_DATE]) <minCount:
        return None 
    # get sequence with list of unique pangolin lineages and how many times they appear in each dataset
    sequence1 = DF1[env.META_PANGOLIN].drop_duplicates().value_counts()
    
    
    sequence2 = DF2[env.META_PANGOLIN].drop_duplicates().value_counts()
    

    # if both have a value at the same index, result is 1, else 0
    lesser_values_series = sequence1.combine(sequence2,min,fill_value=0)
    #print(lesser_values_series)
    return round(((2*lesser_values_series.sum())/(sequence1.sum()+sequence2.sum()))*100,4)


def renkonen_similarity_index_self_diff_dates(PLZ,start1,end1, start2, end2, minCount):
    # https://en.wikipedia.org/wiki/Renkonen_similarity_index
    DF1 = dataService.get_all_in_plz(PLZ)
    DF1 = DF1[(DF1[env.META_SEQUENCE_DATE] >= start1) & (DF1[env.META_SEQUENCE_DATE] <= end1)]
    DF2 = dataService.get_all_in_plz(PLZ)
    DF2 = DF2[(DF2[env.META_SEQUENCE_DATE] >= start2) & (DF2[env.META_SEQUENCE_DATE] <= end2)]
    # get sequence with list of unique pangolin lineages and how many times they appear in each dataset
    sequence1 = DF1[env.META_PANGOLIN].value_counts()
    sequence1Total = sequence1.sum()
    sequence1 = sequence1.apply(lambda x:x/sequence1Total)
    
    sequence2 = DF2[env.META_PANGOLIN].value_counts()
    sequence2Total = sequence2.sum()
    sequence2 = sequence2.apply(lambda x:x/sequence2Total)

    if(sequence1Total < minCount or sequence2Total < minCount):
        return None 

    # if both have a value at the same index, add the smaller of the two 
    lesser_values_series = sequence1.combine(sequence2,min, fill_value=0)
    
    return round(lesser_values_series.sum()*100,4)

def renkonen_similarity_index_self(PLZ,start,end):
        DF1 = dataService.get_all_in_plz(PLZ)
        DF1 = DF1[(DF1[env.META_SEQUENCE_DATE] >= start) & (DF1[env.META_SEQUENCE_DATE] <= end)]
        DF2 = dataService.get_all_in_plz(PLZ)
        DF2 = DF2[(DF2[env.META_SEQUENCE_DATE] <= start) | (DF2[env.META_SEQUENCE_DATE] >= end)]
        # get sequence with list of unique pangolin lineages and how many times they appear in each dataset
        sequence1 = DF1[env.META_PANGOLIN].value_counts()
        sequence1Total = sequence1.sum()
        sequence1 = sequence1.apply(lambda x:x/sequence1Total)
    
        sequence2 = DF2[env.META_PANGOLIN].value_counts()
        sequence2Total = sequence2.sum()
        sequence2 = sequence2.apply(lambda x:x/sequence2Total)

        # if both have a value at the same index, add the smaller of the two 
        lesser_values_series = sequence1.combine(sequence2,min, fill_value=0)
    
        return round(lesser_values_series.sum()*100,4)

def renkonen_similarity_index(PLZ1, PLZ2, start, end):
    # https://en.wikipedia.org/wiki/Renkonen_similarity_index
    DF1 = dataService.get_all_in_plz(PLZ1)
    DF1 = DF1[(DF1[env.META_SEQUENCE_DATE] >= start) & (DF1[env.META_SEQUENCE_DATE] <= end)]
    DF2 = dataService.get_all_in_plz(PLZ2)
    DF2 = DF2[(DF2[env.META_SEQUENCE_DATE] >= start) & (DF2[env.META_SEQUENCE_DATE] <= end)]
    # get sequence with list of unique pangolin lineages and how many times they appear in each dataset
    sequence1 = DF1[env.META_PANGOLIN].value_counts()
    sequence1Total = sequence1.sum()
    sequence1 = sequence1.apply(lambda x:x/sequence1Total)
    
    sequence2 = DF2[env.META_PANGOLIN].value_counts()
    sequence2Total = sequence2.sum()
    sequence2 = sequence2.apply(lambda x:x/sequence2Total)

    # if both have a value at the same index, add the smaller of the two 
    lesser_values_series = sequence1.combine(sequence2,min, fill_value=0)
    
    return round(lesser_values_series.sum()*100,4)

def bray_curtis_single_PLZ(PLZ1, start, end):
    # https://en.wikipedia.org/wiki/Bray%E2%80%93Curtis_dissimilarity
    DF1 = dataService.get_all_in_plz(PLZ1)
    DF1 = DF1[(DF1[env.META_SEQUENCE_DATE]>=start) & (DF1[env.META_SEQUENCE_DATE]<=end)]
    DF2 = dataService.get_all_in_plz(PLZ1)
    DF2 = DF2[(DF2[env.META_SEQUENCE_DATE]<start) | (DF2[env.META_SEQUENCE_DATE]>end)]
    # get sequence with list of unique pangolin lineages and how many times they appear in each dataset
    sequence1 = DF1[env.META_PANGOLIN].value_counts()
    sequence2 = DF2[env.META_PANGOLIN].value_counts()

    # if both have a value at the same index, add the smaller of the two 
    lesser_values_series = sequence1.combine(sequence2,min, fill_value=0)

    lesser_value = lesser_values_series.sum()
    
    # add the total count of pangolin lineages in both
    total_value = sequence1.sum() + sequence2.sum()

    return round((2 * lesser_value) / (total_value), 4)


# returns the Bray-Curtis dissimilarity of two given PLZ in a given date range
def bray_curtis_PLZ(PLZ1,PLZ2, start, end):
    # https://en.wikipedia.org/wiki/Bray%E2%80%93Curtis_dissimilarity
    DF1 = dataService.get_all_in_plz(PLZ1)
    DF1 = DF1[(DF1[env.META_SEQUENCE_DATE]>=start) & (DF1[env.META_SEQUENCE_DATE]<=end)]
    DF2 = dataService.get_all_in_plz(PLZ2)
    DF2 = DF2[(DF2[env.META_SEQUENCE_DATE]>=start) & (DF2[env.META_SEQUENCE_DATE]<=end)]
    # get sequence with list of unique pangolin lineages and how many times they appear in each dataset
    sequence1 = DF1[env.META_PANGOLIN].value_counts()
    sequence2 = DF2[env.META_PANGOLIN].value_counts()

    # if both have a value at the same index, add the smaller of the two 
    lesser_values_series = sequence1.combine(sequence2,min, fill_value=0)

    lesser_value = lesser_values_series.sum()
    
    # add the total count of pangolin lineages in both
    total_value = sequence1.sum() + sequence2.sum()

    return round((2 * lesser_value) / (total_value), 4)
        