# import os
# import sys

# visualizations_dir = os.path.dirname(os.path.dirname(os.path.abspath("visualizations")))
# sys.path.append(visualizations_dir) # In case of error, put manually the path visualizations 

from src import app
from src.config import settings
# application.run(debug=True,port=8558,host='0.0.0.0')
application.run(debug=True,port=8558)

if __name__ == "__main__":
    debug=False
    if settings.ENV == "local":
        debug=True
    
    # app.run(debug=True,port=8558)
    app.run(host='0.0.0.0',port=8558,debug=debug)