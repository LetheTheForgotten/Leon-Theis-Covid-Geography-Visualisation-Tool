@ECHO OFF
echo checking if enviroment exists
echo ------------------------------
if exist datVizEnv\ (

    echo enviroment is present
	echo -----------------------
	echo Initializing enviroment
	echo -----------------------
	activate ./datVizEnv
    echo Starting Server
	echo -----------------------
    python runserver.py
) else (
    echo enviroment not present
	echo ----------------------
    echo creating enviroment
	echo ----------------------
    conda env create --prefix ./datVizEnv --file path-to-yml.yml --yes
    echo enviroment created
	echo ---------------------
	echo Initializing enviroment
	echo -----------------------
	activate ./datVizEnv
    echo Starting server
	echo ---------------------
    python runserver.py
)


