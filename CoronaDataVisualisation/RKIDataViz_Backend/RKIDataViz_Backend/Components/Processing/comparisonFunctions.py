"""exists as a wrapper for various functions to translate raw data into format usable by plotly or other graph visualisation libraries"""
import itertools
import random
import subprocess
import pandas as pd
import numpy as np
import datetime
import skimage.io as sio

import plotly.express as pltx
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go



from ..Enviroment_Variables import enviroment as env 

from .DataService import dataService

from ..Processing import GenomeAnalyser as gAn
from ..Processing import GeographyAnalyser as GeoAn
from RKIDataViz_Backend.Components.Processing.MetaDataAnalyser import bray_curtis_PLZ, bray_curtis_single_PLZ, renkonen_similarity_index, renkonen_similarity_index_self, renkonen_similarity_index_self_diff_dates, sorensen_dice_coefficent_self_diff_dates


# Creates a Map Graph with distance displays from given coordinates
def create_map_figure(latDict, longDict, PLZDict):  
    geoFig = go.Figure()
    
    permList = list()
    #makes sure number of plz is in acceptable range
    if(len(PLZDict)<env.DISTANCE_GRAPH_CAP):
        for i in range(0, len(longDict)):
            permList.append([longDict[i], latDict[i], PLZDict[i]])
    
        if(len(permList) > 1):
            for p in itertools.combinations(permList, 2):
                geoFig.add_trace(go.Scattergeo(
                    showlegend=False,
                    lat = [p[0][1], p[1][1]],
                    lon = [p[0][0], p[1][0]],
                    mode = 'lines',
                    line = dict(width = 1, color = 'black'),
                    hoverinfo = 'text',
                    textposition = 'top center'
                    )
                )
                # ensures that plz is in geodata set
                if(np.isnan(p[0][1]) or np.isnan(p[0][0]) or np.isnan(p[1][0]) or np.isnan(p[1][1])):
                    continue
                else:
                    geoFig.add_trace(go.Scattergeo(
                    showlegend = False,
                    lat = [(p[0][1] + p[1][1]) / 2],
                    lon = [(p[0][0] + p[1][0]) / 2],
                    textposition = "top center",
                    mode = "text",
                    marker = dict(
                        size = 3,
                        color = "blue",
                        line_color = 'blue',
                        line_width = 0.25, 
                        sizemode = 'area'),
                        text = str(int(GeoAn.find_distance(p[0][2], p[1][2]))) + " km",
                        textfont = {
                            "color" : 'blue',
                            "family" : 'Comic Sans',
                            "size" : 14
                        }
                    )
                )
        
    geoTrace = go.Scattergeo( 
        showlegend = False, 
        lon = longDict, 
        lat = latDict, 
        text = PLZDict, 
        textfont = {
            "color" : 'purple',
            "family" : 'Comic Sans',
            "size" : 14
        },
        textposition = "top center",
        mode = "markers+text",
        marker = dict(
            size = 10,
            color = "purple",
            line_color = 'black',
            line_width = 0.5,
            sizemode = 'area'
        )
    )
    
    geoFig.add_trace(geoTrace)
      
    return geoFig

# Generates colours for data points 
def generate_colour_dictionary(valueList, frameName = None):
    colors = dict()
    
    # frameName only present if dataframe
    if frameName != None:
        for j in valueList[frameName].unique():
            newColour = '#' + hex(random.randrange(0, 2 ** 24))[2:]

            while ((newColour in colors.values()) or (len(newColour) != 7)):
                newColour = '#' + hex(random.randrange(0, 2 ** 24))[2:]
                
            colors[j] = newColour
        
        return colors
    
    else:
        for j in valueList:
            newColour = '#' + hex(random.randrange(0, 2 ** 24))[2:]

            while ((newColour in colors.values()) or (len(newColour) != 7)):
                newColour = '#' + hex(random.randrange(0, 2 ** 24))[2:]
            
            colors[j] = newColour
                
        return colors

# translate plotly express objects into subgraph objects
def translate_express_to_graph_object(graphList, distance = None, pangolinDistance = None):
    legendGroups = []
    specs = []
    titles = []
    
    if(distance is not None and pangolinDistance is not None and len(graphList)==1):
        specs.append( 
            [
                {"type" : graphList[0].data[0].type}, 
                {"type" : distance.data[0].type}
            ] 
        )
        specs.append( 
           [ 
                    {}, 
                    {"type" : pangolinDistance.data[0].type} 
           ]
        )
        
        titles.append(graphList[0].layout.title.text)
        titles.append("Distance Between PLZ & Weekly Change in Makeup")
    
    elif(distance is not None):
        specs.append( 
            [
                {"type" : graphList[0].data[0].type}, 
                {"type" : distance.data[0].type}
            ] 
        )
        
        titles.append(graphList[0].layout.title.text)
        titles.append("Distance Between PLZ")
    
    else:
        specs.append( 
            [ 
                {"type" : graphList[0].data[0].type}, 
                {}
            ]
        )
        titles.append(graphList[0].layout.title.text)
        titles.append("")
        
    for i in range(1,len(graphList)):
        if(pangolinDistance is not None and i == 1):
            specs.append( 
                [ 
                    {"type" : graphList[i].data[0].type}, 
                    {"type" : pangolinDistance.data[0].type} 
                ]
            )
            titles.append(graphList[i].layout.title.text)
            titles.append("Renkonen Indexes between PLZ")
            
            continue
        
        specs.append( 
            [ 
                {"type" : graphList[i].data[0].type},
                {}
            ]
        )
        
        titles.append(graphList[i].layout.title.text)
        titles.append("")

    rowCount = len(graphList)    

    if len(graphList) == 1 :
        vertical_spacing = 0.3
        if pangolinDistance is not None:
            rowCount=2
    else:
        vertical_spacing = (1 / (len(graphList) - 1 )) * 0.2

    fig = make_subplots(
        rows = rowCount, 
        cols = 2, 
        subplot_titles = titles, 
        specs = specs, 
        vertical_spacing = (vertical_spacing)
    )

    if(distance is not None):
        for trace in range(len(distance.data)):
            fig.append_trace(distance.data[trace], row = 1, col = 2)
            
    if(pangolinDistance is not None):
        for trace in range(len(pangolinDistance.data)):
            fig.append_trace(pangolinDistance.data[trace], row = 2, col = 2)
            
    for i, figure in enumerate(graphList):
        for trace in range(len(figure.data)):
            if(figure.data[trace].type != "table" and figure.data[trace].type != "image" and figure.data[trace].type!='pie'):
                if(figure.data[trace].legendgroup not in legendGroups):
                    fig.append_trace(figure.data[trace], row = i + 1, col = 1,)
                    legendGroups.append(figure.data[trace].legendgroup)
                else:
                    figure.data[trace].showlegend = False          
                    fig.append_trace(figure.data[trace], row = i + 1, col = 1)
            else:
                fig.append_trace(figure.data[trace], row = i + 1, col = 1)
                
        # adds rangeslider if present - ensures using plots that don't have rangesliders doesn't break the subplot
        if(figure.layout.xaxis["rangeslider"]["visible"]):
            fig.update_xaxes(
                row = i + 1, 
                col = 1, 
                rangeslider = figure.layout.xaxis["rangeslider"], 
                rangeslider_thickness = 30 / (len(graphList) * 600)
            )
            
        if (figure.layout.xaxis["range"] != None):
            fig.update_xaxes(
                row = i + 1,
                col = 1,
                range = figure.layout.xaxis["range"]
            )
            
    for i in fig.layout.annotations:
        i.update(font_color = "white")    
    
    fig.update_layout(
        paper_bgcolor = "#5F5F5F", 
        title_font_color = "white", 
        height = len(graphList) * env.GRAPH_SIZE, 
        font_color = "white"
    )
    
    return fig

# translates images into subgraph object
def translate_images_to_graph_object(graphList):
    legendGroups = []
    specs = []
    titles = []
    
    for i in range(0,len(graphList)) :
        specs.append(
            [
                {"type" : graphList[i].data[0].type}
            ]
        )
        titles.append(graphList[i].layout.title.text)

    if len(graphList) == 1:
        vertical_spacing = 0.3
    else:
        vertical_spacing = (1 / (len(graphList) - 1)) * 0.2
    
    fig = make_subplots(
        rows = len(graphList), 
        cols = 1, 
        subplot_titles = titles, 
        specs = specs, 
        vertical_spacing = (vertical_spacing)
    )

    for i, figure in enumerate(graphList):
        for trace in range(len(figure.data)):
            if(figure.data[trace].type != "table" and figure.data[trace].type != "image"):
                if(figure.data[trace].legendgroup not in legendGroups):
                    fig.append_trace(figure.data[trace], row = i + 1, col = 1)
                    legendGroups.append(figure.data[trace].legendgroup)
               
                else:
                    figure.data[trace].showlegend = False
          
                    fig.append_trace(figure.data[trace], row = i + 1, col = 1)
            else:
                fig.append_trace(figure.data[trace], row = i + 1, col = 1)
        
        #adds rangeslider if present - ensures using plots that don't have rangesliders doesn't break the subplot
        if(figure.layout.xaxis["rangeslider"]["visible"]):
            fig.update_xaxes(row = i + 1, 
                             col = 1, 
                             rangeslider = figure.layout.xaxis["rangeslider"], 
                             rangeslider_thickness = 30 / (len(graphList) * 600)
                             )
        
        if (figure.layout.xaxis["range"] != None):
            fig.update_xaxes(row = i + 1, 
                             col = 1, 
                             range = figure.layout.xaxis["range"]
                             )
    
    for i in fig.layout.annotations:
        i.update(font_color = "white")
    
    fig.update_layout(paper_bgcolor = "#5F5F5F", 
                      title_font_color = "white", 
                      height = len(graphList) * env.GRAPH_SIZE, 
                      font_color = "white"
                      )

    return fig;

# creates a graph for each PLZ selected with the frequency of each pangolin lineage x time as data points
# DATA:
# PLZ: list{selected,postal_code}
# pangolins:{lineage,count,selected]}
# minsamples: number
# start:Date
# end:Date
def PLZScatterPlotByPLZ(data):
    startDate = data['start']
    
    if(startDate != None):
        startDate = np.datetime64(data['start'],'ns')
    endDate = data['end']
    
    if(endDate != None):
        endDate =  np.datetime64(data['end'],'ns')
    
    numOfPLZ = len(data["PLZ"])
    
    graphNameList = []

    if (numOfPLZ == 0 or len(data['pangolins']) == 0):
        return None

    # lists for subgraph
    figList = []    
    dfList = []
    
    # dicts to make distance graphs
    latDict = []
    longDict = []
    PLZDict = []

    # helper variables for parsing
    colorsDict = {}
    lineageList = []
    countList = []
    
    # filter for pangolin lineages selected 
    for i in data['pangolins']:
        # check if count matches minumum count
            if(i['count'] > data['minsamples']):
                lineageList.append(i['lineage'])
                countList.append(i['count'])
            
        
    presentLineages = pd.Series(index = countList, data = lineageList)    

    for i in range(0,len(data["PLZ"])):
        graphName = ""
        
        #line graphs require a DF that is a list of each x/y pair and its value, have to manually count and plot points
        #using a dictionary for ease of translation later
        plotDict = {"x": [], "y": [], "name": []}
        
        #get PLZ
        PLZ = data["PLZ"][i]["postal_code"]
        graphName = PLZ
        
        #make dataframe
        DF = dataService.metaData.getInPostalCode(PLZ)
        
        # makes sure colours of data points remain consistent
        tmpcolors = generate_colour_dictionary(DF, env.META_PANGOLIN)
        tmpcolors.update(colorsDict)
        colorsDict = tmpcolors.copy()
        
        
        # seeds latitude and longitude for distance graph
        latlongtmp = GeoAn.get_coordinates(PLZ)
        
        latDict.append(latlongtmp[0])
        longDict.append(latlongtmp[1])
        
        PLZDict.append(PLZ)

        # plotly requires an integer to sum in the DF
        DF["count"] = [1] * len(DF)
        
       # finds dates present to seed values
        presentDates = pd.Series(DF[env.META_SEQUENCE_DATE].unique()).sort_values(ascending = True)
        
        # filters out datapoints not in given date range
        if (startDate != None):
            presentDates = presentDates.where(presentDates >= startDate).dropna()
            # error output if graph does not exist in date range
            if(len(presentDates) == 0):
                
                figList.append(
                    go.Figure(
                        data = [
                            go.Table(
                                header = dict(values = ['WARNING']),
                                cells = dict(
                                    values = [["" + PLZ + " has no viable data within the chosen date range"]]
                                )
                            )
                        ]
                     )
                )
                
                continue
            graphName = graphName + " starting at: " + str(startDate)[:10]
            
        if (endDate != None):
            presentDates = presentDates.where(presentDates <= endDate).dropna()
            if(len(presentDates) == 0):
                figList.append(
                    go.Figure(
                        data = [
                            go.Table(
                                header=dict(values = ['WARNING']),
                                cells = dict(
                                    values = [["" + PLZ + " has no viable data within the chosen date range"]]
                                )
                            )
                        ]
                    )
                )
                
                continue 
            graphName = graphName + " ending at: " + str(endDate)[:10]
        
        graphNameList.append(graphName)
        
        #count every unique occurence and add to dict
        for i in presentLineages:
            for j in presentDates:
                plotDict["x"].append(j)
                plotDict["name"].append(i)
                plotDict["y"].append(DF[(DF[env.META_PANGOLIN] == i) & (DF[env.META_SEQUENCE_DATE] == j)].count().values[0])
                
        plotDF = pd.DataFrame(plotDict)

        dfList.append(plotDF)

    dateStart = datetime.datetime(2100,1,1)
    dateEnd = datetime.datetime(1970,1,1)     

    # finds first and last date in dataset
    for i in dfList:
        tmp = i['x'].agg(['min', 'max'])
        dateStart = min(dateStart, tmp['min'])
        dateEnd = max(dateEnd, tmp['max'])
    
    
    dateRange = pd.Series(pd.date_range(dateStart, dateEnd, freq = 'D'))
    dateRange.name = "dateRange"
    counter = 0
    for i in dfList:
        mergedDF = pd.merge_ordered(
                        dateRange, 
                        i, 
                        how = 'left', 
                        left_on = "dateRange", 
                        right_on = 'x', 
                        fill_method='ffill'
                     )
        
        intermFig = pltx.line(
                        mergedDF, 
                        title = graphNameList[counter], 
                        x = "x", 
                        y = "y", 
                        line_group = "name", 
                        color = "name", 
                        markers = True, 
                        color_discrete_map = colorsDict
                    )
        intermFig.update_xaxes(
                    rangeslider_visible = True, 
                    range = [dateStart, dateEnd]
                  )
        
        counter += 1
        
        figList.append(intermFig)
    
    ####-------distance graphs------###    
    distanceGraph = create_map_figure(latDict,longDict,PLZDict) 

    returnedFig = translate_express_to_graph_object(figList, distanceGraph)
    returnedFig.update_geos(
                fitbounds="locations"
         )
    
    return pio.to_json(returnedFig)

# creates a line plot per pangolin lineage where data points are how many times it appeared in a plz
# DATA:
# PLZ: list{selected,postal_code}
# pangolins:{lineage,count,selected]}
# minsamples: number
# start:Date
# end:Date
def PLZScatterPlotByPangolin(data):
    startDate = data['start']
    if(startDate != None):
        startDate = np.datetime64(data['start'], 'ns')

    endDate = data['end']
    if(endDate != None):
        endDate =  np.datetime64(data['end'], 'ns')
        
    # len of DF used often, made variable
    numOfPLZ = len(data["PLZ"])
    
    # parse data into DF
    if (numOfPLZ == 0 or len(data['pangolins']) == 0):
        return None
    
    figList = []
    
    # dicts to make distance graphs
    latDict = []
    longDict = []
    PLZDict = []
    linDict = {}
    
    lineageList = []
    countList = []
    # filter for pangolin lineages selected 
    for i in data['pangolins']:
        # check if count matches minumum count
            if(i['count'] > data['minsamples']):
                lineageList.append(i['lineage'])
                countList.append(i['count'])
            
        
    presentLineages = pd.Series(index = countList, data = lineageList)
    
    for i in range(0,len(data["PLZ"])):
        PLZ = data["PLZ"][i]["postal_code"]
       
        
        #make dataframe
        DF = dataService.metaData.getInPostalCode(PLZ)
        
        # add lineages not already in linDict to linDict
        for i in presentLineages:
            if i not in linDict:
                # for every loop of plzs: 
                # x = when
                # y = how many at time x
                # name = PLZ
                # graphs will be generated after by looping through each entry of linDict
                linDict[i] = {"x":[], "y":[], "name":[]}
    linColours = generate_colour_dictionary(linDict.keys())
                
        
    for i in range(0, len(data["PLZ"])):
        
        # get PLZ
        PLZ = data["PLZ"][i]["postal_code"]

        # make dataframe
        DF = dataService.metaData.getInPostalCode(PLZ)
        
        # retrive coordinates for distance graph
        latlongtmp = GeoAn.get_coordinates(PLZ)
        latDict.append(latlongtmp[0])
        longDict.append(latlongtmp[1])
        PLZDict.append(PLZ)

        # plotly requires a counter to sum up things
        DF["count"] = [1] * len(DF)
                
        presentDates = pd.Series(DF[env.META_SEQUENCE_DATE].unique()).sort_values(ascending = True)
        
        if (startDate != None):
            presentDates = presentDates.where(presentDates >= startDate).dropna()
            if(len(presentDates) == 0):
                continue

        if (endDate != None):
            presentDates = presentDates.where(presentDates <= endDate).dropna()
            if(len(presentDates) == 0):
                continue 

        # count every unique occurence and add to dict
        for i in presentLineages:
            for j in presentDates:
                linDict[i]["x"].append(j)
                linDict[i]["name"].append(PLZ)
                linDict[i]["y"].append(
                          DF[(DF[env.META_PANGOLIN] == i) & (DF[env.META_SEQUENCE_DATE] == j)].count().values[0]
                          )
                
        
    
    # convert dict into a list of dataframes - one for each key
    linDataFrameList = []
    for i in linDict:
        linDataFrameList.append([i, pd.DataFrame(linDict[i])])
    

    dateStart = datetime.datetime(2100,1,1)
    dateEnd = datetime.datetime(1970,1,1)     
    
    # finds first and last date present
    for i in linDataFrameList:
        tmp = i[1]['x'].agg(['min', 'max'])
        dateStart = min(dateStart, tmp['min'])
        dateEnd = max(dateEnd, tmp['max'])
    
    
    dateRange = pd.Series(pd.date_range(dateStart, dateEnd, freq = 'D'))
    dateRange.name = "dateRange"
    for i in linDataFrameList:
        mergedDF = pd.merge_ordered(
                        dateRange, 
                        i[1], 
                        how = 'left', 
                        left_on = "dateRange", 
                        right_on = 'x', 
                        fill_method = 'ffill'
                    )
        
        intermFig = pltx.line(
                        mergedDF, 
                        title = i[0], 
                        x = "x", 
                        y = "y", 
                        line_group = "name", 
                        color = "name", 
                        markers=True, 
                        color_discrete_map = linColours
                    )
        
        intermFig.update_xaxes(rangeslider_visible = True, range = [dateStart,dateEnd])
        
        figList.append(intermFig)
    
    ####-------distance graphs------###    
    distanceGraph = create_map_figure(latDict, longDict, PLZDict)

    returnedFig = translate_express_to_graph_object(figList, distanceGraph)
    returnedFig.update_geos(
                        fitbounds="locations"
               )
    
    return pio.to_json(returnedFig)



# creates a pie chart of the pangolin lineages of a given PLZ and date range
# DATA:
# PLZ:list {selected, postal_code}
# startDate : string '1969-12-31T23:00:00.000Z'
# endDate : string
# minPercentage:int
# renkonen : boolean -> if false generate pie charts, if true generate change over time graphs
def pangolinPieChart(data):
    renkonen = data['renkonen']

    startDate = data['startDate']
    if(startDate != None):
        startDate = np.datetime64(startDate, 'ns')

    endDate = data['endDate']
    if(endDate != None):
        endDate =  np.datetime64(endDate, 'ns')
        
    #len of DF used often, made variable
    numOfPLZ = len(data["PLZ"])

    minPercent = data["minPercentage"] / 100    

    minRenCount = data["minPercentage"]    

    #parse data into DF
    if (numOfPLZ == 0):
        return None 
    
    figList = list()

    latList = []
    longList = []
    PLZList = []
    
    if renkonen:
        if (datetime.datetime.strptime(endDate.astype('str')[:-10], '%Y-%m-%dT%H:%M:%S') - datetime.datetime.strptime(startDate.astype('str')[:-10], '%Y-%m-%dT%H:%M:%S')).days <= 7:
            dateRange=pd.date_range(start=startDate, end=endDate, freq="D")
            if(len(dateRange)<=3):
                dateRange=None
        else:    
            dateRange=pd.date_range(start=startDate, end=endDate, freq="7D")
            
        for i in range(0, len(data["PLZ"])):
        
            PLZ=data["PLZ"][i]["postal_code"]
        
            latlongtmp = GeoAn.get_coordinates(PLZ)
            latList.append(latlongtmp[0])
            longList.append(latlongtmp[1])
            PLZList.append(PLZ)
            # dates
            x = []
            # renkonen similarity
            y = []
            # sorensen dice coefficent
            z = []
            # datetime iterable
        
            if(dateRange is not None):
                for i in range(2,len(dateRange)):
                        x.append("KW"+str(dateRange[i-2].week)+" - "+str(dateRange[i-1].week)+" "+str(dateRange[i-2].year))
                        y.append(renkonen_similarity_index_self_diff_dates(PLZ,dateRange[i-2],dateRange[i-1],dateRange[i-1],dateRange[i], minRenCount))
                        z.append(sorensen_dice_coefficent_self_diff_dates(PLZ,dateRange[i-2],dateRange[i-1],dateRange[i-1],dateRange[i], minRenCount))
            intermFig =   pltx.line(x = x, y = y, title="relative rate of change (Weekly) for "+PLZ, markers=True, ) 
            intermFig.add_traces(go.Scatter(x = x, y = z, mode="markers", name="sorosen DC",line_color='#800080', showlegend=False))
            figList.append(intermFig)
    else:

        for i in range(0, len(data["PLZ"])):
        
            PLZ=data["PLZ"][i]["postal_code"]
        
            latlongtmp = GeoAn.get_coordinates(PLZ)
            latList.append(latlongtmp[0])
            longList.append(latlongtmp[1])
            PLZList.append(PLZ)
        
            
        
            DF = dataService.metaData.getInPostalCodeInDateRange(PLZ, startDate, endDate)
            DF["count"] = [1] * len(DF)
            series = DF[env.META_PANGOLIN].value_counts()
            total = series.sum()
            trivialSeries = series.where((series / total) < minPercent).dropna()
        
            for ind in trivialSeries.index:
                DF = DF.replace(ind, "other (>" + str(minPercent) + "%)")
             
            figList.append(pltx.pie(
                DF, 
                values = 'count', 
                names = env.META_PANGOLIN, 
                title = "pangolin lineages in " +
                            PLZ + 
                            " between " + 
                            str(startDate)[:10] + 
                            " and " + 
                            str(endDate)[:10] + 
                            ""
                            )
            )
    
    distanceFig = create_map_figure(latList, longList, PLZList)
    
    PLZDistanceList = []
    
    for i in range(0, len(data['PLZ'])):
        PLZDistanceList.append(data['PLZ'][i]['postal_code'])
    
    pangolinDistanceFig = None;
    if len(data['PLZ']) > 1:
        brayscurtis = []
        brayscurtis.append(PLZDistanceList)
        for j in PLZDistanceList:
            tmpCurt = []
            
            for i in PLZDistanceList:
                tmpCurt.append(renkonen_similarity_index(j, i, startDate, endDate))
            
            brayscurtis.append(tmpCurt)
            
        tmpList = PLZDistanceList.copy()
        
        tmpList.insert(0,"")
        
        pangolinDistanceFig = go.Figure(
                    data = [
                         go.Table( 
                             name = "Renkonen similarity index Between Selected PLZ", 
                             header = dict(values = tmpList, fill_color = "#0B2044"), 
                             cells = dict(values = brayscurtis,fill_color = "#2D3B53"))
                         ]
                    )    
        
    elif((len(data['PLZ']) == 1) and (startDate!=None or endDate!=None)):
        # dates
        x = []
        # renkonen similarity
        y = []
        # sorensen dice coefficent
        z = []
        # datetime iterable
        if (datetime.datetime.strptime(endDate.astype('str')[:-10], '%Y-%m-%dT%H:%M:%S') - datetime.datetime.strptime(startDate.astype('str')[:-10], '%Y-%m-%dT%H:%M:%S')).days <= 7:
            dateRange=pd.date_range(start=startDate, end=endDate, freq="D")
            if(len(dateRange)<=3):
                dateRange=None
        else:    
            dateRange=pd.date_range(start=startDate, end=endDate, freq="7D")
        if(dateRange is not None):
            for i in range(2,len(dateRange)):
                    x.append("KW"+str(dateRange[i-2].week)+" - "+str(dateRange[i].week)+" "+str(dateRange[i-2].year))
                    y.append(renkonen_similarity_index_self_diff_dates(data['PLZ'][0]['postal_code'],dateRange[i-2],dateRange[i-1],dateRange[i-1],dateRange[i], minRenCount))
                    z.append(sorensen_dice_coefficent_self_diff_dates(data['PLZ'][0]['postal_code'],dateRange[i-2],dateRange[i-1],dateRange[i-1],dateRange[i], minRenCount))
        distanceFig =   pltx.line(x = x, y = y, title="relative rate of change (Weekly)", markers=True, ) 
        distanceFig.add_traces(go.Scatter(x = x, y = z, mode="markers", name="sorosen DC",line_color='#800080', showlegend=False))
    returnedFig = translate_express_to_graph_object(figList, distanceFig, pangolinDistanceFig)
    
    
    returnedFig.update_geos(fitbounds="locations")
    
    
    return pio.to_json(returnedFig)

# gets MSA of a given sequence
# DATA
# Seq: list of dict: {'postal_code', 'selected', 'pang_lineage', 'sequence_id', 'date_sequenced'}
# gap_pentalty: number
# extension_penalty : number
def multipleSequenceAlignment(data,stdoutList):
    if(len(data['Seq']) <= 0):
       return None
    
    tmpSeqs = data['Seq']
    seqList = []
    for i in tmpSeqs:
        seqList.append(i['sequence_id'])
        
    path = dataService.get_Muscle_Fasta_File(seqList)
    
    gAn.multiple_sequence_alignment(path, data['timeout'], stdoutList)
    
    indexes = gAn.find_gap_indexes()
    
    figList = []
    
    specs = []
    
    for i in indexes:
        specs.append([{"type" : "image"}])
    
    if len(indexes) == 1:
        vertical_spacing = 0.3
    else:
        vertical_spacing = (1 / (len(indexes) - 1)) * 0.2
        
    subPlot = make_subplots(
        rows = len(indexes), 
        cols = 1, 
        specs = specs, 
        vertical_spacing = (vertical_spacing)
        )

    stdoutList.append("processing MSA File...")
    ## for this to work you gotta set conda in your path variable 
    for i in range(0,len(indexes)):
        mv = (r"conda run pymsaviz -i " + 
              env.MUSCLE_OUT_FILE_PATH + 
              " -o MSA_picture_output_" + str(i) + ".png" +
              " --start " + str(indexes[i][0]) + 
              " --end " + str(indexes[i][1]) + 
              " --show_consensus --show_count --color_scheme Taylor --dpi 500"
              )
        
        stdoutList.append("running in CMD: \n")
        stdoutList.append(mv + " \n")
        
        subprocess.run(mv,                          
                       stdout = subprocess.PIPE,
                       stderr = subprocess.PIPE,
                       shell = True,
                       bufsize = 1)
        
        stdoutList.append("done \n")
        
        
        figList.append(
            pltx.imshow(
                sio.imread("MSA_picture_output_" + str(i) + ".png"), 
                title = "gap between " + str(indexes[i][0]) + " and " + str(indexes[i][1])
                )
            )
        
       
    stdoutList.append("generating graph...")
    subPlot = translate_images_to_graph_object(figList)

    return pio.to_json(subPlot)


# does pairwise sequence alignment on 2+ sequences
# DATA
# "Seq": Seq;
#      "mismatch": mismatchPenalty,
#      "gap": gapPenalty,
#      "extension":extensionPenalty
# "showAlign" : boolean
def pairWiseSequenceAlignment(data):
    
    showAlign = data['showAlign']
    
    if(len(data['Seq']) < 2):
        return None
    
    if(len(data['Seq']) == 2):
        sequences = dataService.get_sequence_pair(data['Seq'][0]['sequence_id'], data['Seq'][1]['sequence_id'])
        
        result = gAn.two_sequence_alignment(
            [data['Seq'][0]['sequence_id'], data['Seq'][1]['sequence_id']], 
            sequences, 
            data['match'], 
            data['mismatch'], 
            data['gap'], 
            data['extension']
            )
        
        with open(env.PAIRWISE_SEQUENCE_DOWNLOAD_PATH, 'w') as f:
            f.write(result[0])
            f.write("\n\n aligned at the indexes of: \n" + result[2]['aligned indexes'])
            f.write(result[1])
            
        f.close()
        
        if(showAlign):
            return result[0] + "\n\n" + "aligned at the indexes of: \n" + result[2]['aligned indexes'] + "\n" + result[1]
        else:
            return result[0]
        
    else:
        seqList = dataService.get_multiple_seqences(data['Seq'])
        idList = []
        for i in range(len(data['Seq'])):
            idList.append(data['Seq'][i]['sequence_id'])
        
        result = gAn.pairwise_sequence_alignment_multiple(
            seqList, 
            data['match'], 
            data['mismatch'], 
            data['gap'], 
            data['extension'], 
            idList
            )
        
        output = ""
        
        with open(env.PAIRWISE_SEQUENCE_DOWNLOAD_PATH, 'w') as f:
            total = 0
            for i in result:
                total += i[2]['score']
            
            average = total / len(seqList)
            
            output += ("" + str(len(seqList)) + 
                       " Sequences Compared with each other \n\nAverage Score: " + str(average) + 
                       "\n\nFor Full Alignments Please Download the txt File "+
                       "\n\nSorted By Score: \n\n")
            
            f.write(output)
            
            #lambda opens list, retreives score 
            result.sort(key = lambda a : a[2]["score"])

            for i in range(0, int(len(result))):
                tmpOutput = "" + str(i) + ": \n" + result[i][0] + "\n"
                tmpAlign = "with Alignment: \n" + result[i][1]
                
                f.write(tmpOutput)
                f.write("\naligned at the indexes of: \n" + result[i][2]['aligned indexes'] + "\n")
                f.write(tmpAlign)
                
                output += tmpOutput + "\n \n"
            
            f.close()
        return output
 