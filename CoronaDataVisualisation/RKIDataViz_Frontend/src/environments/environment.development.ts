const apiURL = 'http://localhost:60530'
export const environment = {
  apiURL: apiURL,
  DOWNLOAD_SELECTED_PATH: apiURL + '/downloadSelected',
  DOWNLOAD_SELECTED_GETTER_PATH: apiURL + '/downloadSelectedgetter',
  DOWNLOAD_FASTA_PATH: apiURL + '/downloadFasta',
  DOWNLOAD_PAIRWISE_SEQUENCE_PATH: apiURL + '/downloadTXT',
  GET_GEO_JSON_PATH: apiURL + '/geoJSON',
  GET_PLZ_LIST_PATH: apiURL + "/getPLZList",
  GET_SEQ_TABLE_FROM_PLZ_PATH: apiURL + "/getSeqTable/",
  CREATE_GRAPH_PATH: apiURL + "/createGraph",
  CHECK_GRAPH_SERVICE_STATUS_PATH: apiURL + "/getGraph",
  GET_PLZ_OF_PANGOLINS_PATH: apiURL + '/getPLZsofPangolins',
  GET_PANGOLINS_OF_PLZ_PATH: apiURL + '/getPangolinsOfPLZ',
  GET_SEQ_LIST_FROM_PLZ_PATH: apiURL + '/getSeqList/',
  PERSISTENT_DATA_PATH: apiURL + '/persistentData/',
  PERSISTENT_DATA_CLEAR_PATH: apiURL + '/persistentDataClear',
  DOWNLOAD_ADDRESS_JSON: apiURL + '/downloadAddrJSON',
  DOWNLOAD_SELECTED_META_PATH: apiURL + '/downloadSelectedMeta',
  DOWNLOAD_SELECTED_META_GETTER_PATH:apiURL + '/downloadSelectedMetagetter',

  //---------------------------------------------------------------//
  GRAPH_JOB_STARTED: "job started",
  GRAPH_ALREADY_RUNNING: "job already running",
  GRAPH_FUNCT_NOT_RECOGNIZED: "not recognized function",
  GRAPH_NO_JOB_RUNNING: "no job running",
  GRAPH_JOB_STILL_RUNNING: "job still running",
  GRAPH_GET_RESULT_ERROR: "get result in graph error",
  GRAPH_JOB_DONE: "job done",
};

