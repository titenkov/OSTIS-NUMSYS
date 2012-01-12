
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
Created on 18.12.2009

@author: Denis Koronchik
'''
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as ois

from suit.cf import BaseEditMode
from suit.cf import BaseViewMode
from suit.cf.TextInput import TextInput
from suit.core.objects import Object
from geom_objects import GeometryPoint
from geom_objects import GeometryLineSection
from geom_objects import GeometryTriangle

import suit.cf.utils as comutils
import suit.core.render.engine as render_engine

class GeometryEditMode(BaseEditMode):
    
    # states
    ES_Move         =   BaseEditMode.ES_Count + 1
    ES_LineCreate   =   ES_Move + 1
    ES_CircleCreate =   ES_LineCreate + 1
    ES_LengthChange =   ES_CircleCreate + 1
    ES_Count        =   ES_LengthChange + 1   
    
    def __init__(self, _logic):
        BaseEditMode.__init__(self, _logic, "Geometry edit")
        
        # last scroll position
        self.last_scroll_pos = None
        
        # grid align mode
        self.grid_align = True
        self.mouse_pos = (0, 0)
        
        # objects we works with
        self.highlighted_obj = None
        # current edit state
        self.state = GeometryEditMode.ES_None
        # current object we worked with
        self.active_object = None
        # line creation mode
        self.__pointSpirit = GeometryPoint()
        self.__pointSpirit.setState(Object.OS_Normal)
        self.__pointSpirit.setScale(ogre.Vector3(0.5, 0.5, 0.5))
        self.__lineSpirit = GeometryLineSection()
        self.__lineSpirit.setState(Object.OS_Normal)        
        self.__lineSpirit.setEnd(self.__pointSpirit) 
        self.__lineBegin = None
        
    def __del__(self):
        BaseEditMode.__del__(self) 
        
    def _highlight(self):
        """Highlighting object under mouse
        """
        mobjects = self._logic._getSheet()._getObjectsUnderMouse(self.mouse_pos)
        obj = None
        if len(mobjects) > 0:
            obj = mobjects[0][1]
        
        if (obj is None) and (self.highlighted_obj is None):    return 
        if (obj is self.highlighted_obj):   return
        
        # change highlight
        if self.highlighted_obj:
            self.highlighted_obj.resetState()
#            if self.highlighted_obj._getSelected():
#                self.highlighted_obj.setState(Object.OS_Selected)
#            else:
#                self.highlighted_obj.setState(Object.OS_Normal)
        self.highlighted_obj = obj
        if self.highlighted_obj:    self.highlighted_obj.setState(Object.OS_Highlighted)
    
    def _getMousePos(self, _state):
        """Returns mouse position based on state and align mode
        @return: mouse position
        @rtype: tuple(int, int)
        """
        if self.grid_align:
            return self._logic.positionMouseToGrid((_state.X.abs, _state.Y.abs))
        else:
            return (_state.X.abs, _state.Y.abs)
        
    def _onMouseMoved(self, _evt):
        """Mouse moved notification event
        """
        if BaseEditMode._onMouseMoved(self, _evt):  return True
      
        mstate = _evt.get_state()
        mpos = self._getMousePos(mstate)
        self.mouse_pos = (mstate.X.abs, mstate.Y.abs)
        
        if self.state is GeometryEditMode.ES_Move:
            self.active_object.setPosition(render_engine.pos2dTo3dIsoPos(mpos))
            return True
        
        elif self.state is GeometryEditMode.ES_LineCreate:
            self.__pointSpirit.setPosition(render_engine.pos2dTo3dIsoPos(mpos))
            self._updateLineSpirits()
            self._highlight()
            return True
        elif self.state is GeometryEditMode.ES_CircleCreate:
            radius = self.active_object.getPosition().distance(render_engine.pos2dTo3dIsoPos(mpos))
            self.active_object.setRadius(radius)
        
        self._highlight()
        
        return False
        
    def _onMousePressed(self, _evt, _id):
        """Event on mouse button pressed
        """
        if BaseEditMode._onMousePressed(self, _evt, _id):   return True
        
        mstate = _evt.get_state()
        mpos = self._getMousePos(mstate)

        # getting objects under mouse
        mobjects = self._logic._getSheet()._getObjectsUnderMouse(True, True, self.mouse_pos)

        if _id == ois.MB_Right:
            # none any mode
            if self.state is GeometryEditMode.ES_None:
                # creating point if there is no any objects under mouse
                if len(mobjects) is 0:
                    obj = self._logic.createPoint(mpos)
                    sheet = self._logic._getSheet()
                    sheet.addChild(obj)
                    return True
                else:
                    obj = comutils._getFirstObjectTypeFromList(mobjects, [GeometryPoint])
                    if obj is not None:
                        self.state = GeometryEditMode.ES_LineCreate
                        self.__lineSpirit.setBegin(obj)
                        sheet = self._logic._getSheet()
                        sheet.sceneNodeChilds.addChild(self.__lineSpirit.sceneNode)
                        sheet.sceneNodeChilds.addChild(self.__pointSpirit.sceneNode)
                        self.__lineBegin = obj
                        self.__pointSpirit.setPosition(render_engine.pos2dTo3dIsoPos(mpos))
                        self._updateLineSpirits()
                        return True
            # on line creation mode finishing line
            elif self.state is GeometryEditMode.ES_LineCreate:
                obj = comutils._getFirstObjectTypeFromList(mobjects, [GeometryPoint])
                sheet = self._logic._getSheet()
                if obj is not None:
                    # creating line
                    line = self._logic.createLineSection(self.__lineBegin, obj)
                    sheet.addChild(line)
                    
                # removing state
                self.state = GeometryEditMode.ES_None
                sheet.sceneNodeChilds.removeChild(self.__lineSpirit.sceneNode)
                sheet.sceneNodeChilds.removeChild(self.__pointSpirit.sceneNode)
                self.__lineBegin = None
                    
            
        elif _id == ois.MB_Left:
            # if there is an any object under mouse, then starts moving
            if len(mobjects) > 0 and self.state is GeometryEditMode.ES_None:
                self.active_object = comutils._getFirstObjectTypeFromList(mobjects, [GeometryPoint])
                if self.active_object is not None:
                    self.state = GeometryEditMode.ES_Move
                    self._selectObject(self.active_object)
                else:
                    # selecting first object under mouse
                    self._selectObject(mobjects[0][1])
                
                return True
            elif self.state is GeometryEditMode.ES_CircleCreate:
                self.active_object = None
                self.state = GeometryEditMode.ES_None
            
        return False
                 
            
    def _onMouseReleased(self, _evt, _id):
        """Event on mouse button released
        """
        if BaseEditMode._onMouseReleased(self, _evt, _id):  return True
        
        mstate = _evt.get_state()
        mpos = self._getMousePos(mstate)
        
        if _id == ois.MB_Left:
            
            # moving state finishing
            if self.state is GeometryEditMode.ES_Move:
                self.state = GeometryEditMode.ES_None
#                self._selectObject(self.active_object)
                self.active_object = None                
        
        return False
    
    def _onKeyPressed(self, _evt):
        """Event on key pressed
        """
        if _evt.key == ois.KC_DELETE:
            return True
        
        if BaseEditMode._onKeyPressed(self, _evt):  return True
        
        key = _evt.key
        
        if key == ois.KC_C and isinstance(self._logic._getSheet().getSelected()[0], GeometryPoint):
            self.state = GeometryEditMode.ES_CircleCreate
            self.active_object = self._logic.createCircle(self._logic._getSheet().getSelected()[0], 3.0)
            self._logic._getSheet().addChild(self.active_object)     
            
        if key == ois.KC_T:
            selected = self._logic._getSheet().getSelected()
               
            if len(selected) == 3:
                # check if selected objects are lines
                lines = True
                for obj in selected:
                    if not isinstance(obj, GeometryLineSection):
                        lines = False
            
                if lines:
                    triangle = self._logic.createTriangle(selected)
                    self._logic._getSheet().addChild(triangle)
                    
        if key == ois.KC_L:
            selected = self._logic._getSheet().getSelected()
            if len(selected) > 0 and isinstance(selected[0], GeometryLineSection):
                self.state = GeometryEditMode.ES_LengthChange
                self.length_changer = TextInput(selected[0], self._length_change_callback, str(selected[0].getLength()))                
        
        return False
    
    def _onKeyReleased(self, _evt):
        """Event key released
        """
        if BaseEditMode._onKeyReleased(self, _evt): return True
        
        return False
    
    def _length_change_callback(self, _object, _value):
        """Callback on line length changing
        """
        self.state = GeometryEditMode.ES_None
        if _value is not None:
            try:
                v = float(str(_value))
                _object.setLength(v)
            except ValueError:
                print "Non-numeric value found %s" % str(_value)
        del self.length_changer
    
    def _updateLineSpirits(self):
        """Updates spirit objects used in line creation mode
        """
        self.__pointSpirit.needUpdate = True
        self.__pointSpirit._update(0)
        self.__lineSpirit.needUpdate = True
        self.__lineSpirit._update(0)

            