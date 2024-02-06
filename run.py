import os
import sys

visualizations_dir = os.path.dirname(os.path.dirname(os.path.abspath("visualizations")))
sys.path.append(visualizations_dir) # In case of error, put manually the path visualizations 

from app import app as application
# application.run(debug=True,port=8558,host='0.0.0.0')
application.run(debug=True,port=8558)