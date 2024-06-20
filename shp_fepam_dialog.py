# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ShpFEPAMDialog
                                 A QGIS plugin
 Une os shapes para FEPAM
        begin                : 2024-06-20
        copyright            : (C) 2024 by Romário Moraes Carvalho Neto
        email                : romariocarvalho@hotmail.com
 ***************************************************************************/
"""

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'shp_fepam_dialog_base.ui'))


class ShpFEPAMDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(ShpFEPAMDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
