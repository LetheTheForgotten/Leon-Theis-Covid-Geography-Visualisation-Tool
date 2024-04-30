from flask import Blueprint, request, send_file

import numpy as np
import pandas as pd

from ..Enviroment_Variables import enviroment as env
from ..Enviroment_Variables import ControllerEnv as pathEnv

from RKIDataViz_Backend.Components.Processing.DataService import dataService


from ..Processing import GeographyAnalyser as geo




###----------ToDos-----------##


#------------------HTTP Requests----------------#
baseDataControllerAPI = Blueprint('baseDataServiceAPI', __name__)

#gets sequences associated with postal code
@baseDataControllerAPI.route(pathEnv.GET_SEQ_LIST_FROM_PLZ_PATH)
def getSeqListFromPLZ(PLZ):
    return dataService.get_all_seq_in_PLZ(PLZ).to_json(orient="records")

#gets sequences associated with postal code in format displayed in frontend 
@baseDataControllerAPI.route(pathEnv.GET_SEQ_TABLE_FROM_PLZ_PATH)
def getSeqTableFromPLZ(PLZ):

    DF=dataService.get_all_seq_attributes_in_PLZ(PLZ)

    DF.reset_index(inplace=True)
    DF=DF[[env.META_POSTAL,env.META_SEQUENCE_ID,env.META_PANGOLIN,env.META_SEQUENCE_DATE]]
    DF.insert(0,"selected",np.full(len(DF[env.META_POSTAL]),False))
    
    DF=DF.rename(columns={"selected":"selected",env.META_POSTAL:"postal_code",env.META_SEQUENCE_DATE:"date_sequenced",env.META_PANGOLIN:"pang_lineage",env.META_SEQUENCE_ID:"sequence_id"})
    
    return DF.to_json(orient="records")

@baseDataControllerAPI.route(pathEnv.GET_GEO_JSON_PATH)
def getGeoJSON():
    """gets geoJSON from python"""
    return geo.shape_frame_global

@baseDataControllerAPI.route(pathEnv.GET_PLZ_LIST_PATH)
def getPLZList():
    
    return geo.plz_list_global

@baseDataControllerAPI.route(pathEnv.GET_PANGOLINS_OF_PLZ_PATH,methods=['POST'])
def getPangolinsofPLZ():
    body = request.json
    
    countseries = pd.Series()
    
    if len(body) == 0:
        return None
    
    maxes = []
    mins = []
    
    for i in body:
        DF = dataService.get_all_in_plz(i['postal_code'])
        
        maxes.append(DF[env.META_SEQUENCE_DATE].max())
        mins.append(DF[env.META_SEQUENCE_DATE].min())
        
        counts = DF[env.META_PANGOLIN].value_counts()
        
        countseries = countseries.combine(counts,lambda a,b:a+b,fill_value=0)
        
    countseries.value_counts()

    DF = pd.DataFrame(countseries)
    
    DF = DF.reset_index()
    
    DF["selected"] = [False]*len(DF[0])
    DF["maxOrMin"] = [""]*len(DF[0])
    
    DF.loc[0,["maxOrMin"]] = min(mins)
    DF.loc[1,["maxOrMin"]] = max(maxes)
    
    DF = DF.rename(columns = {'index':"lineage",0:"count"})
    
    return DF.to_json(orient = "records")

@baseDataControllerAPI.route(pathEnv.GET_PLZ_OF_PANGOLINS_PATH,methods = ['POST'])
def getPLZofPangolins():
    
    body = request.json
    
    countseries = pd.Series()
    PLZcounters = pd.Series()
    
    if len(body) == 0:
        return None
    
    maxes = []
    mins = []
    
    for i in body:
        DF = dataService.get_all_in_plz(i['postal_code'])
        
        maxes.append(DF[env.META_SEQUENCE_DATE].max())
        mins.append(DF[env.META_SEQUENCE_DATE].min())
        
        counts = DF[env.META_PANGOLIN].value_counts()

        PLZcounters = PLZcounters.combine(counts,lambda a,b:a if b<=0 else a+1 ,fill_value=0)
        countseries = countseries.combine(counts,lambda a,b:a+b,fill_value=0)
       

    countseries.value_counts()
  
    
    DF = pd.DataFrame(countseries)
    
    DF["present_PLZ"] = PLZcounters
    
    DF = DF.reset_index()
   
    DF["selected"] = [False]*len(DF[0])
    DF["maxOrMin"] = [""]*len(DF[0])

    DF.loc[0,["maxOrMin"]] = min(mins)
    DF.loc[1,["maxOrMin"]] = max(maxes)
    
    DF = DF.rename(columns = {'index':"lineage",0:"count"})
    
    return DF.to_json(orient = "records")

@baseDataControllerAPI.route(pathEnv.DOWNLOAD_FASTA_PATH)
def downloadFasta():
    return send_file(env.MSA_OUTPUT_DOWNLOAD_PATH,as_attachment = True)

@baseDataControllerAPI.route(pathEnv.DOWNLOAD_PAIRWISE_SEQUENCE_PATH)
def downloadPairwiseSequence():
    return send_file(env.PAIRWISE_SEQUENCE_DOWNLOAD_PATH,as_attachment = True)

@baseDataControllerAPI.route(pathEnv.DOWNLOAD_ADDRESS_JSON)
def downloadJsonPath():
    return send_file(env.FILEREADER_JSON_PATH_OUT,as_attachment = True)

@baseDataControllerAPI.route(pathEnv.DOWNLOAD_SELECTED_PATH,methods=['post'])
def downloadSelected():
    
    body = request.json
    
    with open(env.SELECTED_SEQUENCE_DOWNLOAD_PATH, 'w') as f:
            for i in body:
                seq = dataService.genomeData[i['sequence_id']]
                f.write('>' + i['sequence_id'] + "\n")
                f.write(seq + " \n")
    f.close()
    return {}
    
    
@baseDataControllerAPI.route(pathEnv.DOWNLOAD_SELECTED_GETTER_PATH,methods = ['get'])
def downloadSelectedGetter():
    return send_file(env.SELECTED_SEQUENCE_DOWNLOAD_PATH,as_attachment = True)

@baseDataControllerAPI.route(pathEnv.DOWNLOAD_SELECTED_META_PATH,methods=['post'])
def downloadSelectedMeta():
    
    body = request.json
    output = pd.DataFrame(body)
    output['date_sequenced'] = output['date_sequenced'].map(lambda x: np.datetime64(x,'ms'))
    output.to_csv(env.SELECTED_META_DOWNLOAD_PATH)
    
    return {}
    
    
@baseDataControllerAPI.route(pathEnv.DOWNLOAD_SELECTED_META_GETTER_PATH,methods = ['get'])
def downloadSelectedMetaGetter():
    return send_file(env.SELECTED_META_DOWNLOAD_PATH,as_attachment = True)


persistentData = dict()

@baseDataControllerAPI.route(pathEnv.PERSISTENT_DATA_PATH, methods=['post'])
def postPersistentData(key):
    persistentData[key]=request.data
    return {}

@baseDataControllerAPI.route(pathEnv.PERSISTENT_DATA_CLEAR_PATH, methods=['post'])
def deletePeristentData():
    persistentData.clear()
    return {}


@baseDataControllerAPI.route(pathEnv.PERSISTENT_DATA_PATH, methods = ['get'])
def getPersistentData(key):
    if key in persistentData:
        return persistentData[key]
    else:
        return {},"404 key not found"

