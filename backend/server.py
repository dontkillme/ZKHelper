from waitress import serve
    
from zkhelper.wsgi import application
    
if __name__ == '__main__':
    serve(application, port='8001')