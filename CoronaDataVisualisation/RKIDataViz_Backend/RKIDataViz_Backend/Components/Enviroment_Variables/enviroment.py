#Files

#path of main backend file
OS_PATH = r"C:\Users\Leon\Documents\GitHub\ba_leon_theis\CoronaDataVisualisation\RKIDataViz_Backend"

#Sequencing Data
FASTA_FILE = r"B:\fasta\fasta\SARS-CoV-2-Sequenzdaten_Deutschland.fasta"

#MetaData
METADATA_FILE = r"B:\fasta\fasta\SARS-CoV-2-Sequenzdaten_Deutschland.tsv"

#data for map shapes and postal codes 
# sourced from: https://www.suche-postleitzahl.org/downloads
POSTAL_CODE_AREAS = r"Data\GeoData\plz-5stellig.shp"

POSTAL_CODE_LOCATION_NAME = r"Data\GeoData\zuordnung_plz_ort.csv"

POSTAL_CODE_POPULATION = r"Data\GeoData\plz_einwohner.csv"


#test data
test_data = r"B:\fasta\fasta\fastatestdata.fasta"

tsv_test_data = r"B:\fasta\fasta\MetaDataTest.tsv"

#set if json should be used for filereader
FILEREADER_JSON_PATH_READ = OS_PATH + r"\Data\Setup\addressDict.json"

#where the filereader will post the JSON to when done
FILEREADER_JSON_PATH_OUT = OS_PATH + r"\Data\Setup\addressDict.json"

#number of threads
THREAD_COUNT = 10

#names of columns in metadata
META_POSTAL = 'DL.POSTAL_CODE'
META_SEQUENCE_ID = 'SEQUENCE.ID'
META_SEQUENCE_DATE = 'SEQUENCE.DATE_OF_SAMPLING'
META_PANGOLIN = 'PANGOLIN.LINEAGE_LATEST'

##int for asci code of character used to determine sequence name in parsed file
##ie fasta uses '>' thus the value is 62
HEADER_CHAR = 62

#size for subplots in comparisonfunctions.py
GRAPH_SIZE = 600

#urls for muscle
MUSCLE_EXE = OS_PATH + r"\Data\Muscle\muscle.exe"

MUSCLE_IN_FILE_PATH = OS_PATH + r"\Data\Muscle\MSA_Input2.fasta"

MUSCLE_OUT_FILE_PATH = OS_PATH + r"\Data\Muscle\MSA_Output.fasta"

MSA_IMAGE_FILE_PATH = OS_PATH + r"\Data\Muscle\MSA_Image.png"

#download location of MSA result for user download
#requires an absolute path
MSA_OUTPUT_DOWNLOAD_PATH = OS_PATH + r"\Data\Muscle\MSA_Output.fasta"

#download location of fasta of selected sequences
#requires an absolute path
SELECTED_SEQUENCE_DOWNLOAD_PATH = OS_PATH + r"\Data\Downloads\downloadedSequences.fasta"

#download location of fasta of selected sequences
#requires an absolute path
SELECTED_META_DOWNLOAD_PATH = OS_PATH + r"\Data\Downloads\downloadedMeta.csv"

#download of pairwise sequence alignments
#requires an absolute path
PAIRWISE_SEQUENCE_DOWNLOAD_PATH = OS_PATH + r"\Data\pairwiseAlign.txt"

#maximum number of postal codes until distance graph no longer generated
DISTANCE_GRAPH_CAP = 10

#location code for pgeocode
PGEOCODE_COUNTRY_CODE = 'de'