"""
This script runs the RKIDataViz_Backend application using a development server.
"""

from os import environ
from RKIDataViz_Backend import app
import webbrowser






if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '60530'))
    except ValueError:
        PORT = 60530
    print("\n\n\n#--------------------------------------#")
    print("#--------------------------------------#")    
    print("#app running at: http://"+HOST+":"+str(PORT)+"#")
    print("#--------------------------------------#")
    print("#--------------------------------------#\n\n\n")
    webbrowser.open_new("http://"+HOST+":"+str(PORT))
    app.run(HOST, PORT)
