#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import numpy as np
import pandas as pd
import os
import csv

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_dataframe (self):
        excel_file = pd.read_excel(self.file_path)
        return excel_file
