# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PrintYour3DDialog
                                 A QGIS plugin
 With this plugin you could print 3D model from your data.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-02-28
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Szymek Ślęczka
        email                : szymex23@o2.pl
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.core import QgsMapLayerProxyModel
from qgis.PyQt.QtWidgets import QFileDialog
#import from main_code
from .create_model.pySTL import scaleSTL, pySTL
from .create_model import create_model


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'Print_Your_3D_dialog_base.ui'))


class PrintYour3DDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        self.stopped = False
        self.plugin_dir = os.path.dirname(__file__)

        super(PrintYour3DDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        #create buttons
        self.btnGraph.clicked.connect(self.pixels)
        self.btnGraph.clicked.connect(self.stretching)
        self.btnGraph.clicked.connect(self.delaunay)
        self.btnGraph.clicked.connect(self.graph3d)
        self.btnSelect.clicked.connect(self.select_output_file)
        self.btnScale.clicked.connect(self.scale)
        self.btnSave.clicked.connect(self.pixels)
        self.btnSave.clicked.connect(self.delaunay)
        self.btnSave.clicked.connect(self.loading)
        self.btnSave.clicked.connect(self.saver)
        self.btnShape.clicked.connect(self.shape)
        # Fetch the currently loaded layers
        self.layers = self.cmbSelectLayer.currentLayer()
        self.cmbSelectLayer.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.cmbSelectShape.currentLayer()
        self.cmbSelectShape.setFilters(QgsMapLayerProxyModel.VectorLayer)

        #create object of class Create_model
        self.creator = create_model.Create_model(dlg=self, current_layer=self.layers)

        #self.trash_remover() # to zrobic zeby wykywalo sie za kazdym razem

    # methods to create buttons
    # import from main code inside create_model.py

    def pixels(self):
        self.creator.iterator()
    def graph3d(self):
        self.creator.create_graph()
    def stretching(self):
        if self.stopped == False:
            self.creator.stretching()
            self.stopped = True
        return self.stopped
    def delaunay(self):
        self.creator.delaunay()
    def saver(self):
        self.creator.saver()
    def shape(self):
        self.creator.shape(self.plugin_dir)
    def loading(self):
        self.creator.loading()
    def scale(self):
        set_scale = scaleSTL.Scalator(scale_text=self.lineEdit, cmbScale=self.cmbScale) #usunac dlg bo juz jest w dialogu
        set_scale.scaleSTL()
    def scale_print(self):
        print(self.cmbScale.currentText())

    def select_output_file(self):
        filename, _filter = QFileDialog.getSaveFileName(
            self, "Select   output file ", "", '*.stl')
        self.lineEdit.setText(filename)

    def trash_remover(self):
        trash_path = self.plugin_dir+'/TRASH'
        for file in os.listdir(trash_path):
            if file == 'merged.tif': pass
            if file == 'merged.tif.aux.xml': pass
            else: os.remove(trash_path+'\\' +f'{file}')
        #remove = [print('zostaw') if file == 'merged.tif' else os.remove(trash_path+'\\' +f'{file}') for file in os.listdir(trash_path)]
        #return remove
