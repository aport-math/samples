'''
Verifies that the following are installed: Python 3.6.0, pip 10.0.0, Tensorflow 2.0, TkInter 8.6, NumPy 1.14.5, Pandas 1.1, and MatPlotLib 3.0.2.

To add Python (here version 3.6) to Path:
	Press Win+R and type sysdm.cpl
	Go to Advanced >> Envronment Variables...
	Under System Variables, click Path and then Edit...
	Click New and type C:\\Users\\[username]\\AppData\\Local\\Programs\\Python\\Python36 
		as well as C:\\Users\\[username]\\AppData\\Local\\Programs\\Python\\Python36\\Scripts
                (WITH ONLY \ AND NOT \\, was needed here due to unicode issues on Windows)

To install pip (if not installed already):
	Open cmd
	Type the following:
		python -m pip install -U pip

To install Tensorflow on Windows:
	Open cmd
	Type the following:
		python -m pip install tensorflow

To install TkInter:
        Should be included with Python since version 3.1, but if needed download and
            install Anaconda from https://www.anaconda.com/products/individual

To install NumPy on Windows:
	Open cmd
	Type the following:
		python -m pip install numpy

To install SciPy on Windows:
	Open cmd
	Type the following:
		python -m pip install scipy

To install Pandas on Windows:
	Open cmd
	Type the following:
		python -m pip install pandas

To install MatPlotLib on Windows:
	Open cmd
	Type the following:
		python -m pip install -U matplotlib
'''

### Suppress info and warning messages
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

### Version thresholds for Python and required modules
python_version_threshold = '3.6.0'
pip_version_threshold = '10.0.0'
tensorflow_version_threshold = '2.0'
tkinter_version_threshold = '8.6'
numpy_version_threshold = '1.14.5'
scipy_version_threshold = '1.6.0'
pandas_version_threshold = '1.11'
matplotlib_version_threshold = '3.0.2'

### Make sure the current version of Python is sufficiently new
from sys import version_info
python_version = '%d.%d.%d'%(version_info.major, version_info.minor, version_info.micro)
if python_version < python_version_threshold:
    print('ERROR: Installed Python vesion is ' + python_version + \
        '. Please install version ' + python_version_threshold + \
        ' of Python or later.')
else:
    print('Python installation found: version ' + python_version)

### Import required modules, check their version
# pip
try:
    import pip
    if pip.__version__ < pip_version_threshold:
        raise Exception('Error: Installed pip vesion is ' + pip.__version__ + \
            '. Please install version ' + pip_version_threshold + \
            ' of pip or later.')
    print('pip installation found: version ' + pip.__version__)
except ImportError:
    print('ERROR: pip module not found. Please install version ' + \
        pip_version_threshold + ' of pip or later.')
except Exception as error:
    print(error)
    print('\n')
    input('Press Enter to Quit...')
    quit()
except:    
    print('ERROR: Unspecified error in loading pip. Please install version ' + \
        pip_version_threshold + ' of pip or later.')
    print('\n')
    input('Press Enter to Quit...')
    quit()
# Tensorflow
try:
    import tensorflow as tf
    if tf.__version__ < tensorflow_version_threshold:
        raise Exception('ERROR: Installed Tensorflow module vesion is ' + tf.__version__ + \
            '. Please install version ' + tensorflow_version_threshold + \
            ' of Tensorflow or later.')
    print('Tensorflow installation found: version ' + tf.__version__)
except ImportError:
    print('ERROR: Tensorflow module not found. Please install version ' + \
        tensorflow_version_threshold + ' of Tensorflow or later.')
except Exception as error:
    print(error)
    print('\n')
    input('Press Enter to Quit...')
    quit()
except:    
    print('ERROR: Unspecified error in loading Tensorflow. Please install version ' + \
        tensorflow_version_threshold + ' of Tensorflow or later.')
    print('\n')
    input('Press Enter to Quit...')
    quit()
# TkInter
try:
    import tkinter as tk
    if str(tk.TkVersion) < tkinter_version_threshold:
        raise Exception('ERROR: Installed TkInter module vesion is ' + str(tk.TkVersion) + \
            '. Please install version ' + tkinter_version_threshold + \
            ' of TkInter or later.')
    print('TkInter installation found: version ' + str(tk.TkVersion))
except ImportError:
    print('ERROR: TkInter module not found. Please install version ' + \
        str(tkinter_version_threshold) + ' of TkInter or later.')
except Exception as error:
    print(error)
    print('\n')
    input('Press Enter to Quit...')
    quit()
except:
    print('ERROR: Unspecified error in loading TkInter. Please install version ' + \
        str(tkinter_version_threshold) + ' of TkInter or later.')
    print('\n')
    input('Press Enter to Quit...')
    quit()
# NumPy
try:
    import numpy as np
    if np.version.version < numpy_version_threshold:
        raise Exception('ERROR: Installed NumPy module vesion is ' + np.version.version + \
            '. Please install version ' + numpy_version_threshold + \
            ' of NumPy or later.')
    print('NumPy installation found: version ' + np.version.version)
except ImportError:
    print('ERROR: NumPy module not found. Please install version ' + \
        numpy_version_threshold + ' of NumPy or later.')
except Exception as error:
    print(error)
    print('\n')
    input('Press Enter to Quit...')
    quit()
except:    
    print('ERROR: Unspecified error in loading NumPy. Please install version ' + \
        numpy_version_threshold + ' of NumPy or later.')
    print('\n')
    input('Press Enter to Quit...')
    quit()
### SciPy
try:
    import scipy
    if scipy.__version__ < scipy_version_threshold:
        raise Exception('ERROR: Installed SciPy module vesion is ' + scipy.__version__ + \
            '. Please install version ' + scipy_version_threshold + \
            ' of SciPy or later.')
    print('SciPy installation found: version ' + scipy.__version__)
except ImportError:
    print('ERROR: SciPy module not found. Please install version ' + \
        scipy_version_threshold + ' of SciPy or later.')
except Exception as error:
    print(error)
    print('\n')
    input('Press Enter to Quit...')
    quit()
except:    
    print('ERROR: Unspecified error in loading SciPy. Please install version ' + \
        scipy_version_threshold + ' of SciPy or later.')
    print('\n')
    input('Press Enter to Quit...')
    quit()
# Pandas
try:
    import pandas as pd
    if pd.__version__ < pandas_version_threshold:
        raise Exception('ERROR: Installed Pandas module vesion is ' + pd.__version__ + \
            '. Please install version ' + pandas_version_threshold + \
            ' of Pandas or later.')
    print('Pandas installation found: version ' + pd.__version__)
except ImportError:
    print('ERROR: Pandas module not found. Please install version ' + \
        pandas_version_threshold + ' of Pandas or later.')
except Exception as error:
    print(error)
    print('\n')
    input('Press Enter to Quit...')
    quit()
except:    
    print('ERROR: Unspecified error in loading Pandas. Please install version ' + \
        pandas_version_threshold + ' of Pandas or later.')
    print('\n')
    input('Press Enter to Quit...')
    quit()
# Matplotlib
try:
    import matplotlib as mpl
    if mpl.__version__ < matplotlib_version_threshold:
        raise Exception('ERROR: Installed Matplotlib module vesion is ' + mpl.__version__ + \
            '. Please install version ' + matplotlib_version_threshold + \
            ' of Matplotlib or later.')
    print('Matplotlib installation found: version ' + mpl.__version__)
except ImportError:
    print('ERROR: Matplotlib module not found. Please install version ' + \
        matplotlib_version_threshold + ' of Matplotlib or later.')
except Exception as error:
    print(error)
    print('\n')
    input('Press Enter to Quit...')
    quit()
except:    
    print('ERROR: Unspecified error in loading Matplotlib. Please install version ' + \
        matplotlib_version_threshold + ' of Matplotlib or later.')
    print('\n')
    input('Press Enter to Quit...')
    quit()
print('\n')
input('Press Enter to Quit...')
quit()
