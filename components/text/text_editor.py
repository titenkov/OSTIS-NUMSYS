
"""
-----------------------------------------------------------------------------
This source file is part of OSTIS (Open Semantic Technology for Intelligent Systems)
For the latest info, see http://www.ostis.net

Copyright (c) 2010 OSTIS

OSTIS is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OSTIS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with OSTIS.  If not, see <http://www.gnu.org/licenses/>.
-----------------------------------------------------------------------------
"""

'''
Created on 15.05.2010

@author: Denis Koronchick
'''

from suit.core.objects import BaseLogic
import suit.core.render.mygui as mygui
import suit.core.kernel as core
import suit.core.render.engine as render_engine

class TextEditor(BaseLogic):
    
    def __init__(self):
        BaseLogic.__init__(self)
    
    def __del__(self):
        BaseLogic.__del__(self)
        
    def delete(self):
        BaseLogic.delete(self)
        
    def _setSheet(self, _sheet):
        BaseLogic._setSheet(self, _sheet)
        _sheet.eventRootChanged = self._onRootChanged
        _sheet.eventUpdate = self._onUpdate
        
    def _onRootChanged(self, _isRoot):
        """Root changing event callback
        """
        if _isRoot:
            pass
        else:
            pass
    
    def _onUpdate(self, timeSinceLastFrame):
        pass
    