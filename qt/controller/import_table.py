# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-11-13
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from moneyguru.gui.import_table import ImportTable as ImportTableModel
from .table import Table

class ImportTable(Table):
    HEADER = ['Date', 'Description', 'Amount']
    ROWATTRS = ['date_import', 'description_import', 'amount_import']
    DATECOLUMNS = frozenset(['date_import'])
    
    def _getModel(self):
        return ImportTableModel(view=self, import_window=self.dataSource)
    