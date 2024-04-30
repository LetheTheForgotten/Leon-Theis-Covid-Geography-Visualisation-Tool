from flask import Blueprint, request

import threading
import inspect

from ..Enviroment_Variables import ControllerEnv as env

from ..Processing import comparisonFunctions 

NO_JOB_RUNNING = "no job running"
JOB_STILL_RUNNING = "job still running" 
JOB_ERROR = "get result in graph error"

class graphService(object):
    """Service that handles graph display and processing"""
    
    result = None
    stdoutList = []
    loop = None
    


    def startAsyncProssesing(self,function,params):
        if(len(inspect.signature(function).parameters)>1):
            self.result = function(params,self.stdoutList)
        else:
            self.result = function(params)
        
    
    def startProcessing(self,function,params):
        if(self.loop is not None):        
            return False
        
        #reset result
        self.result = None
        self.stdoutList = []
        
        #create new thread
        self.loop = threading.Thread(target = self.startAsyncProssesing,args = (function,params))
        
        #run async operation
        self.loop.start()
        
        return True
        
    def getResults(self):
        
        #if loop is not present no job is running
        if(self.loop is None):
            return NO_JOB_RUNNING

        #if its running its not done
        if(self.loop.is_alive()):
            return JOB_STILL_RUNNING
        
        #if its not running its either failed or done
        self.loop.join();
        
        #if result has remained unchanged there was some kind of error
        if(self.result is None):
            self.loop = None
            return JOB_ERROR
            
        
        #otherwise return result
        else:
            returnValue = self.result
            
            #reset loop and results for safety
            self.result = None
            self.stdoutList = []
            self.loop = None
            
            
            return returnValue
            
GraphService = graphService()

#--------------------------------HTTP Requests-------------------------------------#
graphControllerAPI = Blueprint('graphServiceAPI', __name__)

@graphControllerAPI.route(env.CREATE_GRAPH_PATH, methods=['POST'])
def createGraph():
    
    funct = None
    params = None    
    
    body = request.json
    
    functionName = body["operation"]
    
    funct = getattr(comparisonFunctions,functionName)

    params = body["data"]    

    if (funct is not None):
        if(GraphService.startProcessing(funct,params)):
            return "" , env.GRAPH_JOB_STARTED  
        
        return "" , env.GRAPH_ALREADY_RUNNING
    
    else:
        return "" , env.GRAPH_FUNCT_NOT_RECOGNIZED
    

@graphControllerAPI.route(env.CHECK_GRAPH_SERVICE_STATUS_PATH)
def check_graph_service_status():
    result = GraphService.getResults()
    
    if(result == NO_JOB_RUNNING):
        return "" , env.GRAPH_NO_JOB_RUNNING
    
    if(result == JOB_STILL_RUNNING):
        return "".join(GraphService.stdoutList) , env.GRAPH_JOB_STILL_RUNNING
    
    if(result == JOB_ERROR):
        return "" , env.GRAPH_GET_RESULT_ERROR
    
    return result, env.GRAPH_JOB_DONE