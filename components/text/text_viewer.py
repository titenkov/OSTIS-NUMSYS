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
Created on 09.02.2010

@author: Pavel Karpan
'''

import suit.core.kernel as core
import suit.core.render.engine as render_engine
import suit.core.render.mygui as mygui
import suit.core.objects as objects
from suit.core.kernel import Kernel
from suit.core.objects import BaseLogic
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as ois


def initialize():
    pass


def shutdown():
    pass
    
def _createViever():
    return TextViewer()

class TextViewer(BaseLogic):
    
    def __init__(self):
        """Constructor
        """
        BaseLogic.__init__(self)
        self.statictext = None
        self.isRoot = False
         
        # attach flags
        self.rectAttached = False
        
        # creating rectangle (surface)
#        self.rect = ogre.Rectangle2D(True)
#        self.rect.setCorners(-1.0, 1.0, 1.0, -1.0)
#        self.rect.setRenderQueueGroup(ogre.RENDER_QUEUE_8)
#        self.rect.setBoundingBox(ogre.AxisAlignedBox(ogre.Vector3(-100000.0, -100000.0, -100000.0), ogre.Vector3(100000.0, 100000.0, 100000.0)))
    
    def __del__(self):
        """Destructor
        """        
        BaseLogic.__del__(self)        
        
    def delete(self):
        """Deletion message
        """
        BaseLogic.delete(self)
        # detaching objects
        if self.rectAttached:
            self._getSheet().sceneNodeChilds.detachObject(self.rect)
        self.destroyPanel()
    
    def _onUpdate(self, _timeSinceLastFrame):
        """Logic update
        """
        BaseLogic._update(self, _timeSinceLastFrame)
        self._updateState() 
                    
    def _setSheet(self, _sheet):
        """Sets sheet for a logic
        """
        BaseLogic._setSheet(self, _sheet)
        _sheet.eventRootChanged = self._onRootChanged
        _sheet.eventUpdate = self._onUpdate
        
        self._createArea()
        self.statictext.setCaption(unicode(self.getContent()))
 
    def _onRootChanged(self, isRoot):
        """Root mode switching.
        Creating interface and surface for playing in root mode.
        """        
        if isRoot:
#            self._getSheet().sceneNodeChilds.attachObject(self.rect)
#            self.rectAttached = True            
            self.isRoot = True
            
            # calculating position
            tsize = self.statictext.getTextSize()
            self.statictext.setPosition((render_engine.Window.width - tsize.width) / 2,
                                        (render_engine.Window.height - tsize.height) / 2)
            
            self.statictext.setSize(tsize.width, tsize.height)                                    
        else:
#            if self.rectAttached:
#                self._getSheet().sceneNodeChilds.detachObject(self.rect)
#                self.rectAttached = False
            self.isRoot = False
            self._updateState()
            self.statictext.setSize(91, 91)
    
    def getContent(self):        
        import suit.core.sc_utils as sc_utils
        import suit.core.keynodes as keynodes
        session = core.Kernel.session()
        _addr = self._getSheet()._getScAddr()
        if _addr is not None:
            fmt = sc_utils.getContentFormat(session, _addr)
            
            if fmt.this == keynodes.ui.format_string.this or fmt.this == keynodes.ui.format_term.this:
                value = session.get_content_str(_addr)
            elif fmt.this == keynodes.ui.format_int.this or fmt.this == keynodes.ui.format_real.this:
                value = str(session.get_content_real(_addr))
                
            return value            
			
        return None
    
    def _createArea(self):
#        print dir(mygui)
        self.statictext = render_engine.Gui.createWidgetT("StaticText", "StaticText",
                                                          mygui.IntCoord(0, 0, 91, 91),
                                                          mygui.Align(mygui.ALIGN_VSTRETCH),
                                                          "Main")
        self.statictext.setTextColour(mygui.Colour(0.0, 0.0, 0.0, 1.0))
        #self.statictext.setCaption(self.getContent())
        self.statictext.setNeedMouseFocus(False)        
        
    def destroyPanel(self):        
        if self.statictext:
            render_engine.Gui.destroyWidget(self.statictext)
    
    def _updateState(self):
        
        _sheet = self._getSheet()
        if self.isRoot:
            self.statictext.setVisible(True)
        elif not self.isRoot and _sheet.isContentShow and _sheet.isSceneAttached:
            self.statictext.setVisible(True) 
            pos3d = self._getSheet().getPosition()
            pos2d = render_engine.pos3dTo2dWindow(pos3d)
            self.statictext.setPosition(pos2d[0]-45,pos2d[1]-45)  
        elif not _sheet.isContentShow or not _sheet.isSceneAttached and not self.isRoot:
            self.statictext.setVisible(False)
                    
        return True
