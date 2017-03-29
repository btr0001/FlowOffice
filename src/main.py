import sys

# import PyQt4 QtCore module
from PyQt4.QtCore import * 

if __name__ == '__main__':

    # create application
    app = QCoreApplication( sys.argv )
    app.setApplicationName( 'My PyQt4 QtCore Project' )

    qWarning( 'This is your PYTHON-Qt Console Application: My PyQt4 QtCore Project' )

    # execute application
    sys.exit( app.exec_() )
