# BA Leon Theis

## Description
A locally runnable web application that enables comparison of sequenced COVID-19 data as it relates to their geopgraphical location.\

## Compatability:

Tested on a windows 10 pc with 16 Gb of ram and a AMD Ryzen 5 4600H 3.00 GHz

Untested on linux


# Prerequisites:
Python

https://www.python.org/

Conda

https://www.anaconda.com/download/

Conda must be set as a path variable for full functionality
	
# Build

to build the app requires node.js and the npm package manager

if not already present, install angular using ```npm install -g @angular/cli```

> open ```RKIDataViz_Frontend``` in terminal
>
> run ```ng build --configuration production``` in terminal 
>
> copy the contents of the folder ```RKIDataViz_Frontend\dist\rkidata-viz-frontend\browser``` into ```RKIDataViz_Backend\RKIDataViz_Backend\templates```

two warnings involving a duplicate key "cool" will appear.

this is from the plotly javascript library I am using, its safe to ignore

#Deployment

running does not to my knowledge require node.js or npm installed but this has not been tested on a machine without them

> run using ```RKIDataViz_Backend\RKIDataViz_Backend\run.bat``` 

it is reccomended that ```run.bat``` be run using the command line as it will build the conda enviroment for the app

it is possible that updates to libraries in the conda enviroment breaks the code, as it will always build using the most recent versions.
in /condabackups there is a yaml with the environment used during development, including version numbers.

# Required Files and Environment Variables:

these files must be present for the program to run

## Ensuring Enviromental Variables Function
the variable ```OS_PATH``` must be set to the top folder of the backend for the program to function properly.

this does not require rebuilding, just change the values in ```environment.py```


## Sequencing and Meta Data

> Sequences and Associated Metadata


### Related Environment Variables:

```FASTA_FILE```: fasta by default, parsing method can be changed in \RKIDataViz_Backend\Components\FileIO\GenomeData.py

```METADATA_FILE```: TSV

#### MetaData Enviroment Variables
```META_POSTAL```: postal codes of sequence

```META_SEQUENCE_ID```: associated sequence ID, as found in FASTA_FILE

```META_SEQUENCE_DATE```: date of sequencing

```META_PANGOLIN```	: pangolin lineage by default, theoretically can be any unique string based identifier of lineage


### Source:

https://github.com/robert-koch-institut/SARS-CoV-2-Sequenzdaten_aus_Deutschland


## Geographical Data

> Files for the Shape of the postal codes on the map as well as metadata related to them

### Related Environment Variables:

```POSTAL_CODE_AREAS```: shapefile, contains vector representation of the area of a postal code

```POSTAL_CODE_LOCATION_NAME```: csv, human parseable names of postal code locations

```POSTAL_CODE_POPULATION```: csv, population data of postal code

### Source:

https://www.suche-postleitzahl.org/downloads

## Download Locations

> This application can download files to your system.
> 
> The methodology used requires a full system path to the download location.
> 
> Please have the path end in a file of the specified type.

### Related Enviromental Variables:

```MSA_OUTPUT_DOWNLOAD_PATH```: fasta

```SELECTED_SEQUENCE_DOWNLOAD_PATH```: fasta

```PAIRWISE_SEQUENCE_DOWNLOAD_PATH```: txt


## Thread Count

This program does multithreaded operations.

### Related Enviroment Variable:

```THREAD_COUNT```: int, default value is 10.



