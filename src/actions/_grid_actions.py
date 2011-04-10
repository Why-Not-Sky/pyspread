#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6 on Sun May 25 23:31:23 2008

# Copyright 2008 Martin Manns
# Distributed under the terms of the GNU General Public License
# generated by wxGlade 0.6 on Mon Mar 17 23:22:49 2008

# --------------------------------------------------------------------
# pyspread is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyspread is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyspread.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------


"""
_grid_actions.py
=======================

Module for main main grid level actions.
All non-trivial functionality that results from grid actions
and belongs to the grid only goes here.

Provides:
---------
  1. FileActions: Actions which affect the open grid
  2. TableRowActionsMixin: Mixin for TableActions
  3. TableColumnActionsMixin: Mixin for TableActions
  4. TableTabActionsMixin: Mixin for TableActions
  5. TableActions: Actions which affect table
  6. MacroActions: Actions on macros
  7. UnRedoActions: Actions on the undo redo system
  8. GridActions: Actions on the grid as a whole
  9. SelectionActions: Actions on the grid selection
  10. AllGridActions: All grid actions as a bundle
  

"""

from model._data_array import DataArray
from gui._grid_table import GridTable
from gui._events import *
from lib._interfaces import sign, verify, is_pyme_present

class FileActions(object):
    """File actions on the grid"""
    
    def __init__(self):
        self.main_window.Bind(EVT_COMMAND_GRID_ACTION_OPEN, self.open) 
        self.main_window.Bind(EVT_COMMAND_GRID_ACTION_SAVE, self.save) 

    def validate_signature(self, filename):
        """Returns True if a valid signature is present for filename"""
        
        sigfilename = filename + '.sig'
        
        try:
            dummy = open(sigfilename)
            dummy.close()
        except IOError:
            # Signature file does not exist
            return False
        
        # Check if the sig is valid for the sigfile
        return verify(sigfilename, filename)

    def approve(self, filepath):
        """Sets safe mode if signature missing of invalid"""
        
        if self.validate_signature(filepath):
            post_command_event(self.main_window, SaveModeExitMsg)
            
            statustext = "Valid signature found. File is trusted."
            post_command_event(self.main_window, StatusBarMsg, text=statustext)
            
        else:
            post_command_event(self.main_window, SaveModeEntryMsg)
            
            statustext = "File is not properly signed. Safe mode " + \
                         "activated. Select File -> Approve to leave safe mode."
            post_command_event(self.main_window, StatusBarMsg, text=statustext)

    def open(self, event):
        """Opens a file that is specified in event.attr
        
        Parameters
        ----------
        event.attr: Dict
        \tkey filepath contains file path of file to be loaded
        \tkey interface contains interface class for loading file
        
        """
        
        interface = event.attr["interface"]()
        filepath = event.attr["filepath"]
        
        try:
            interface.open(filepath)
        except IOError:
            statustext = "Error opening file " + filepath + "."
            post_command_event(self.main_window, StatusBarMsg, text=statustext)
            
            return 0
        
        # Make loading safe
        self.approve(filepath)
        
        # Get cell values
        self.grid.data_array.sgrid = interface.get_values()
        
        interface.close()
        
        _grid_table = GridTable(self.grid, self.grid.data_array)
        self.grid.SetTable(_grid_table, True)
    
    def sign_file(self, filepath):
        """Signs file if possible"""
        
        if is_pyme_present() and not self.main_window.safe_mode:
            signature = sign(filepath)
            signfile = open(filepath + '.sig','wb')
            signfile.write(signature)
            signfile.close()
        else:
            msg = 'Cannot sign the file. Maybe PyMe is not installed.'
            short_msg = 'Cannot sign file!'
            self.main_window.interfaces.display_warning(msg, short_msg)

    
    def save(self, event):
        """Saves a file that is specified in event.attr
        
        Parameters
        ----------
        event.attr: Dict
        \tkey filepath contains file path of file to be saved
        \tkey interface contains interface class for saving file
        
        """
        
        interface = event.attr["interface"]()
        filepath = event.attr["filepath"]
        
        interface.save(self.data_array.sgrid, filepath)
        self.sign_file(filepath)


class TableRowActionsMixin(object):
    """Table row controller actions"""

    def set_row_height(self, row, height):
        """Sets row height"""
        
        raise NotImplementedError

    def add_rows(self, row, no_rows=1):
        """Adds no_rows rows before row, appends if row > maxrows"""
        
        raise NotImplementedError

    def delete_rows(self, row, no_rows=1):
        """Deletes no_rows rows"""
        
        raise NotImplementedError


class TableColumnActionsMixin(object):
    """Table column controller actions"""

    def set_col_width(self, row, width):
        """Sets column width"""
        
        raise NotImplementedError

    def add_cols(self, col, no_cols=1):
        """Adds no_cols columns before col, appends if col > maxcols"""
        
        raise NotImplementedError

    def delete_cols(self, col, no_cols=1):
        """Deletes no_cols column"""
        
        raise NotImplementedError


class TableTabActionsMixin(object):
    """Table tab controller actions"""

    def add_tabs(self, tab, no_tabs=1):
        """Adds no_tabs tabs before table, appends if tab > maxtabs"""
        
        raise NotImplementedError

    def delete_tabs(self, tab, no_tabs=1):
        """Deletes no_tabs tabs"""
        
        raise NotImplementedError

class TableActions(TableRowActionsMixin, TableColumnActionsMixin, 
                   TableTabActionsMixin):
    """Table controller actions"""
        
    def OnShapeChange(self, event):
        """Grid shape change event handler"""
        
#        new_rows, new_cols, new_tabs = event.shape
#        old_rows, old_cols, old_tabs = self.pysgrid.shape
#        
#        if new_rows > old_rows:
#            self.add_rows(old_rows, new_rows - old_rows)
#        elif new_rows < old_rows:
#            self.delete_rows(old_rows, old_rows - new_rows)
#        
#        if new_cols > old_cols:
#            self.add_cols(old_cols, new_cols - old_cols)
#        elif new_cols < old_cols:
#            self.delete_cols(old_cols, old_cols - new_cols)
#            
#        if new_tabs > old_tabs:
#            self.add_tabs(old_tabs, new_tabs - old_tabs)
#        elif new_tabs < old_tabs:
#            self.delete_tabs(old_tabs, old_tabs - new_tabs)
#        
#        self.pysgrid.shape = new_rows, new_cols, new_tabs
        
        event.Skip()

    
class MacroActions(object):
    """Macro controller actions"""
        
    def set_macros(selfself, macro_string):
        """Sets macro string"""
    
        raise NotImplementedError


class UnRedoActions(object):
    """Undo and redo operations on grid level"""
    
    def undo(self):
        raise NotImplementedError
        
    def redo(self):
        raise NotImplementedError
        


class GridActions(object):
    """Grid level grid actions"""
    
    def __init__(self):
        self.main_window.Bind(EVT_COMMAND_GRID_ACTION_NEW, self.new)
    
    def new(self, event):
        """Creates a new spreadsheet. Expects data_array in event."""
        
        # Grid table handles interaction to data_array
        self.grid.data_array.sgrid = event.data_array.sgrid
    
        _grid_table = GridTable(self.grid, self.grid.data_array)
        self.grid.SetTable(_grid_table, True)
    
    def zoom(self):
        pass
    
    def get_cursor(self):
        """Returns current grid cursor cell"""
        
        return self.grid.key

    def _switch_to_table(self, newtable):
        """Switches grid to table"""
        
        raise NotImplementedError
#        if newtable in xrange(self.Actions.shape[2]):
#            # Update the whole grid including the empty cells
#            
#            self.grid.current_table = newtable
#            
#            self.grid.ClearGrid()
#            self.grid.Update()
#            
#            self.grid.zoom_rows()
#            self.grid.zoom_cols()
#            self.grid.zoom_labels()
#            
#            post_entryline_text(self.grid, "")

    def set_cursor(self, value):
        """Changes the grid cursor cell."""
        
        if len(value) == 3:
            row, col, tab = value
            self._switch_to_table(tab)
        else:
            row, col = value
        
        if not (row is None and col is None):
            self.grid.MakeCellVisible(row, col)
            self.grid.SetGridCursor(row, col)
        
    cursor = property(get_cursor, set_cursor)
    
class SelectionActions(object):
    """Actions that affect the grid selection"""
    
    def select_cell(self, row, col, add_to_selected=False):
        self.grid.SelectBlock(row, col, row, col, addToSelected=add_to_selected)
    
    def select_slice(self, row_slc, col_slc, add_to_selected=False):
        """Selects a slice of cells
        
        Parameters
        ----------
         * row_slc: Integer or Slice
        \tRows to be selected
         * col_slc: Integer or Slice
        \tColumns to be selected
         * add_to_selected: Bool, defaults to False
        \tOld selections are cleared if False
        
        """
        
        if not add_to_selected:
            self.grid.ClearSelection()
        
        if row_slc == row_slc == slice(None, None, None):
            # The whole grid is selected
            self.grid.SelectAll()
            
        elif row_slc.stop is None and col_slc.stop is None:
            # A block is selcted:
            self.grid.SelectBlock(row_slc.start, col_slc.start, 
                                  row_slc.stop-1, col_slc.stop-1)
        else:
            for row in irange(row_slc.start, row_slc.stop, row_slc.step):
                for col in irange(col_slc.start, col_slc.stop, col_slc.step):
                    self.select_cell(row, col, add_to_selected=True)
    

class AllGridActions(FileActions, TableActions, MacroActions, UnRedoActions, 
                     GridActions, SelectionActions):
    """All grid actions as a bundle"""
    
    def __init__(self, grid, data_array):
        self.main_window = grid.parent
        self.grid = grid
        self.data_array = data_array
        
        FileActions.__init__(self)
        TableActions.__init__(self)
        MacroActions.__init__(self)
        UnRedoActions.__init__(self)
        GridActions.__init__(self)
        SelectionActions.__init__(self)
