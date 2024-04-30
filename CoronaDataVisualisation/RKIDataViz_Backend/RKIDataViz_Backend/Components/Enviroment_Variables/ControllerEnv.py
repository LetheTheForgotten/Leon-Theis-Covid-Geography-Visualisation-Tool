##-----------------------URLS--------------------##

## Base Data Controller
GET_SEQ_LIST_FROM_PLZ_PATH = '/getSeqList/<string:PLZ>'
GET_SEQ_TABLE_FROM_PLZ_PATH = '/getSeqTable/<string:PLZ>'
GET_GEO_JSON_PATH = '/geoJSON'
GET_PLZ_LIST_PATH = '/getPLZList'
GET_PANGOLINS_OF_PLZ_PATH = '/getPangolinsOfPLZ'
GET_PLZ_OF_PANGOLINS_PATH = '/getPLZsofPangolins'
DOWNLOAD_FASTA_PATH = '/downloadFasta'
DOWNLOAD_PAIRWISE_SEQUENCE_PATH='/downloadTXT'
DOWNLOAD_SELECTED_PATH = '/downloadSelected'
DOWNLOAD_SELECTED_GETTER_PATH = '/downloadSelectedgetter'
DOWNLOAD_SELECTED_META_PATH = '/downloadSelectedMeta'
DOWNLOAD_SELECTED_META_GETTER_PATH = '/downloadSelectedMetagetter'
DOWNLOAD_ADDRESS_JSON = '/downloadAddrJSON'

## Graph Controller
CREATE_GRAPH_PATH = "/createGraph"
CHECK_GRAPH_SERVICE_STATUS_PATH = "/getGraph"

## persistent data
#turns out that 65k entries are too much for javascript to parse into a JSON so this is a workaround
PERSISTENT_DATA_PATH='/persistentData/<string:key>'
PERSISTENT_DATA_CLEAR_PATH='/persistentDataClear'

##---------------Graph Return Messages--------------##
GRAPH_JOB_STARTED = "200 job started"
GRAPH_ALREADY_RUNNING = "200 job already running"
GRAPH_FUNCT_NOT_RECOGNIZED = "200 not recognized function"
GRAPH_NO_JOB_RUNNING = "200 no job running"
GRAPH_JOB_STILL_RUNNING =  "200 job still running"
GRAPH_GET_RESULT_ERROR = "200 get result in graph error"
GRAPH_JOB_DONE = "200 job done"

