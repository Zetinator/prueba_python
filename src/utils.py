#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import numpy as np
import pandas as pd
import os
import csv

class Almacen:
    def __init__(self, ID, PDV, info, sub_inventario):
        # setup variables
        self.ID = ID
        self.PDV = PDV
        self.info = info
        self.sub_inventario = sub_inventario
        # llenado de sub inventario
        self.orden_compra = self.info.iloc[:,2:self.info.shape[1]-1]
        # drop the nans by columns
        self.orden_compra = self.orden_compra.dropna(axis=1)


class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_dataframe (self):
        excel_file = pd.read_excel(self.file_path)
        excel_file = excel_file[0:len(excel_file)-1]
        return excel_file

class AlmacenLoader:
    def __init__(self, order_file_path, recepcion_file_path):
        # lee el excel de orden y obtener un dataframe de el
        data = DataLoader(order_file_path)
        self.excel_file = data.load_dataframe()
        # lee el excel de recepcion y obtener un dataframe de el
        self.recibidos_loader = RecepcionLoader(recepcion_file_path)
        # lista de almacenes
        self.almacenes = []

        n = len(self.excel_file)

        # hora de llenar los almacenes de ordenes de compra y de sub inventarios
        for i in range(n):
            self.almacenes.append(Almacen( 
                self.excel_file['Sub inventario'].values[i], 
                self.excel_file['PDV'].values[i], 
                # find row in the dataframe by ID
                self.excel_file.loc[self.excel_file['Sub inventario'] == self.excel_file['Sub inventario'].iloc[i]],
                self.recibidos_loader.load(self.excel_file['Sub inventario'].values[i])
                ))

class RecepcionLoader:
    def __init__(self, file_path):
        # lee el excel y obtener un dataframe de el
        data = DataLoader(file_path)
        self.excel_file = data.load_dataframe()

    def load (self, almacen_ID):
        # find row in the dataframe by ID
        recibidos = self.excel_file.loc[self.excel_file['SUBINVENTARIO'] == almacen_ID]
        # --------------------validaciones--------------------
        # columnas necesarias
        columnas_necesarias = ['SUBINVENTARIO', 'NOMBRE', 'MODELO', 'IMEI', 'FOLIO']
        if not(self.excel_file.columns.isin(columnas_necesarias).all()):
            print('ERROR: Documento de orden de compra no cumple con las columnas necesarias')
        # imei repetido
        if (recibidos['IMEI'].duplicated().any()):
            print('ERROR: Codigos IMEI repetidos')
        # --------------------end_validaciones--------------------

        recibidos = recibidos.set_index('MODELO').stack()
        return recibidos
