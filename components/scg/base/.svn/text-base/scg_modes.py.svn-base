
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
Created on 11.12.2009

@author: Denis Koronchik
'''
from suit.cf import BaseViewMode
from suit.cf import BaseEditMode
from suit.cf import TextInput
import suit.cf.utils as comutils

import suit.core.render.engine as render_engine
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as ois
import suit.core.objects as objects
import scg_alphabet
import scg_objects
import scg_controls
import suit.core.render.mygui as mygui

from suit.cf.VisualMenu import VisualMenu
from suit.cf.VisualMenu import VisualMenuItem
from suit.cf.ToolBar import ToolBar

import scg_environment as env
import scg_utils


# mode show widget
_show_mode_window = None
_show_mode_text = None

def initialize():
    """Initialize mode show widget
    """
    global _show_mode_window
    global _show_mode_text
    _show_mode_window = render_engine.Gui.createWidgetT("Window", "Panel", 
                                                 mygui.IntCoord(0, 0, 0, 0), mygui.Align(),
                                                 "Popup", "")
    _show_mode_text = _show_mode_window.createWidgetT("StaticText", "StaticText",
                                               mygui.IntCoord(7, 7, 0, 0), mygui.Align())

def shutdown():
    """Shutting down mode show widget
    """
    global _show_mode_window
    global _show_mode_text
    render_engine.Gui.destroyWidget(_show_mode_window)
    _show_mode_window = None
    _show_mode_text = None

def _switchMode(_mode):
    """Shows mode description and change environment depend on mode
    """
    global _show_mode_text
    _show_mode_text.setCaption("#FF6633" + unicode(_mode.name))
    size = _show_mode_text.getTextSize()
    _show_mode_window.setSize(size.width + 14, size.height + 14)
    _show_mode_window.setPosition(render_engine.Window.width - size.width - 19,
                                  render_engine.Window.height - size.height - 19)
    _show_mode_text.setSize(size.width, size.height)
    
def hideMode():
    """Makes mode shower invisible
    """
    _show_mode_window.setVisible(False)
    
def showMode():
    """Makes mode shower visible
    """
    _show_mode_window.setVisible(True)

class SCgViewMode(BaseViewMode):
    """Mode that allows user to view and navigate in scg window
    """
    def __init__(self, _logic):
        BaseViewMode.__init__(self, _logic, "View mode")
        
    def __del__(self):
        BaseViewMode.__del__(self)
        
    

# ****************
# * Editor modes *
# ****************
class SCgEditMode(BaseEditMode):
    """Mode that allows user to edit scg-constructions
    
    """
    # states
    ES_Move         = BaseEditMode.ES_Count     # object movement state
    ES_LineCreate   = ES_Move + 1               # line creation mode
    ES_TypeChange   = ES_LineCreate + 1         # type changing mode
    ES_ContType     = ES_TypeChange + 1         # content type changing
    ES_Translate    = ES_ContType + 1           # translate camera position
    ES_ContourCreate= ES_Translate + 1          # contour creation
    ES_Count        = ES_ContourCreate + 1      # count of all states
    
    EM_Select   =   0
    EM_Pair     =   1
    EM_Bus      =   2
    EM_Contour  =   3
    EM_Count    =   4
    
    def __init__(self, _logic):
        BaseEditMode.__init__(self, _logic, "Edit mode")
        
        # mouse objects for line creation mode
        self.line_mode_beg = None
        self.line_mode_obj = scg_alphabet.createSCgNode('mnode')
        self.line_mode_obj.setScale(ogre.Vector3(0.1, 0.1, 0.1))
        self.line_mode_obj.setPosition(ogre.Vector3(0, 0, 0))
        self.line_mode_line = scg_alphabet.createSCgPair('mpair')
        self.line_mode_line.setEnd(self.line_mode_obj)
        self.line_mode_line.setState(objects.Object.OS_Normal)
        # highlighted object
        self.highlighted_obj = None
        
        # widgets
        self.type_combo = None
        self.content_combo = None
        
        # object we worked on in current state
        self.object_active = None
        # current editor state
        self.state = SCgEditMode.ES_None
        # current mouse position
        self.mouse_pos = (0, 0)
        
        # visual menu
        self.vis_menu = None
        self._createVisualMenu()
        
        # 3d navigation mode
        self.rotX = 0.0 
        self.rotY = 0.0
        self.move = ogre.Vector3(0.0, 0.0, 0.0)
        self.moveSpeed = 15.0
        self.moveScale = 1.0
        
        # tool bar
#        self.toolbar = ToolBar()
#        self.toolbar.setVisible(False)
#        self.toolbar.setEnabled(True)
#        for idx in xrange(self.EM_Count):
#            button = self.toolbar.appendButton("", "scg_toolbar_icons.png", idx, (32, 32), (0, 0, 256, 32))
#            button.setCheckable(True)
#            button.setUserData(idx)
#            button.eventPush = self._onToolBarButtonPush
#            
#        self.toolbar.setButtonSize(38)
            
        
    def __del__(self):
        BaseEditMode.__del__(self)
        
        
    def delete(self):
        """Deletion message
        """
        BaseEditMode.delete(self)
        
        self.vis_menu.delete()
        
        self.line_mode_beg = None
        
        self.line_mode_line.delete()
        self.line_mode_line = None
        self.line_mode_obj.delete()
        self.line_mode_obj = None
        
        self.object_active = None
        
        
    def activate(self):
        """Activation message
        """
        BaseEditMode.activate(self)
        self._updateVisualMenu()
        
    def deactivate(self):
        """Deactivation message
        """
        BaseEditMode.deactivate(self)
        self._updateVisualMenu()
        
    def _update(self, timeSinceLastFrame):
        """Updates mode
        """
#        if self.vis_menu.isShow():
        sel_objects = self._logic._getSheet().getSelected()
        n = len(sel_objects)
        if n == 1:
            obj = sel_objects[0]
            self.vis_menu.move(render_engine.pos3dTo2dWindow(sel_objects[0].getPosition()))
        self.vis_menu._update(timeSinceLastFrame)
        
        if not self._ctrl and self.state is SCgEditMode.ES_Translate:
            if self._logic._getSheet().isRoot and render_engine.viewMode is render_engine.Mode_Perspective:
                # processing keyboard input
                if  render_engine._oisKeyboard.isKeyDown(ois.KC_A):
                    self.move.x = -self.moveScale    # Move camera left
        
                if  render_engine._oisKeyboard.isKeyDown(ois.KC_D):
                    self.move.x = self.moveScale    # Move camera RIGHT
        
                if  render_engine._oisKeyboard.isKeyDown(ois.KC_W):
                    self.move.z = -self.moveScale  # Move camera forward
        
                if  render_engine._oisKeyboard.isKeyDown(ois.KC_S):
                    self.move.z = self.moveScale    # Move camera backward
                    
                if  render_engine._oisKeyboard.isKeyDown(ois.KC_Q):
                    self.move.y = self.moveScale  # Move camera up
        
                if  render_engine._oisKeyboard.isKeyDown(ois.KC_E):
                    self.move.y = -self.moveScale    # Move camera down
            
                # updating camera position
                camera = render_engine._ogreCamera
                cameraNode = render_engine._ogreCameraNode
                cameraNode.translate(camera.getOrientation() * self.move)
                camera.yaw(self.rotX)
                camera.pitch(self.rotY)
                self.move = ogre.Vector3(0, 0, 0)
                self.rotX = 0
                self.rotY = 0
        
        
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
            if self.highlighted_obj._getSelected():
                self.highlighted_obj.setState(objects.Object.OS_Selected)
            else:
                self.highlighted_obj.setState(objects.Object.OS_Normal)
        self.highlighted_obj = obj
        if self.highlighted_obj:    self.highlighted_obj.setState(objects.Object.OS_Highlighted)
        
    def _onMouseMoved(self, _evt):
        """Mouse moved event
        """
        mstate = _evt.get_state()
        prev_pos = self.mouse_pos
        self.mouse_pos = (mstate.X.abs, mstate.Y.abs)
        
        
        # move object
        if self.state is SCgEditMode.ES_Move:
            pos = self.move_obj.getPosition()
            #self.move_obj.setPosition((pos[0] + dpos[0], pos[1] + dpos[1]))
            if render_engine.viewMode is render_engine.Mode_Isometric:
                self.move_obj.setPosition(render_engine.pos2dTo3dIsoPos(self.mouse_pos))
            else:
                self.move_obj.setPosition(render_engine.pos2dToViewPortRay(self.mouse_pos).getPoint(25.0))
            if self.vis_menu.isShow():  self.vis_menu.move(self.mouse_pos)
            return True
                
        elif self.state is SCgEditMode.ES_LineCreate:
            pos = render_engine.pos2dTo3dIsoPos(self.mouse_pos)
            self.line_mode_obj.setPosition(pos)
            self._updateLineCreationObjects()
            self._highlight()
            return True
        
        elif self.state is SCgEditMode.ES_Translate:
            if render_engine.viewMode is render_engine.Mode_Isometric:
                render_engine._ogreCameraNode.translate(-mstate.X.rel / float(render_engine.scale2d),
                                                         mstate.Y.rel / float(render_engine.scale2d),
                                                         0.0)
                self._logic._getSheet()._updateChildTexts()
            else:
                self.rotX = ogre.Degree(-mstate.X.rel * 0.13)
                self.rotY = ogre.Degree(-mstate.Y.rel * 0.13)
            #FIXME:    add perspective mode
        
        # scaling
        if self._ctrl and mstate.Z.rel != 0 and render_engine.viewMode == render_engine.Mode_Isometric:
            sc = 1.0 + mstate.Z.rel / 1200.0            
            sheet = self._logic._getSheet()
            sheet.setScale(sheet.getScale() * sc)
        
        self._highlight()
        
        return False
    
    def _onMousePressed(self, _evt, _id):
        """Mouse button pressed event
        """
        mstate = _evt.get_state()
#        self._createNode((mstate.X.abs, mstate.Y.abs))

        # getting objects under mouse
        mobjects = self._logic._getSheet()._getObjectsUnderMouse(True)
        
        
        # * if pressed left button and there is any object under mouse, then
        # start move it
        if _id == ois.MB_Left:
            # check objects under mouse
            if self.state is SCgEditMode.ES_None:
                if len(mobjects) is not 0:
                    self.move_obj = comutils._getFirstObjectTypeFromList(mobjects, [scg_objects.SCgNode, 
                                                                                    objects.ObjectSheet, 
                                                                                    scg_objects.SCgContour])
                    if self.move_obj is not None:
                        self.state = SCgEditMode.ES_Move
                        render_engine._gui_ignore_input_proc_result = True
                        # selecting movable object                       
                        self._selectObject(self.move_obj)
                        return True
                
                    # selecting first object under mouse
                    self._selectObject(mobjects[0][1])
                    
                    return True
               
        
        # * if pressed left button and there are no objects under mouse, then
        # creating new scg-node            
        elif _id == ois.MB_Right:
            # check objects under mouse
            if self.state is SCgEditMode.ES_None:
                if len(mobjects) is 0:
                    self._logic._createNode((mstate.X.abs, mstate.Y.abs))
                    self.state = SCgEditMode.ES_None
                    return True
                else:
                    if self.line_mode_beg is None:
                        self.state = SCgEditMode.ES_LineCreate
                        # setting begin object
                        self.line_mode_beg = mobjects[0][1]
                        self.line_mode_line.setBegin(self.line_mode_beg)
                        self.line_mode_obj.setPosition(render_engine.pos2dTo3dIsoPos((mstate.X.abs, mstate.Y.abs)))
                        # adding to scene
                        sheet = self._logic._getSheet() 
                        render_engine.SceneNode.addChild(sheet.sceneNodeChilds, self.line_mode_line.sceneNode)
                        
                        self._updateLineCreationObjects()
                        
                        return True
                    
            # line creation state
            elif (self.state is SCgEditMode.ES_LineCreate) and (self.line_mode_beg is not None):
                # check if is there 
                if len(mobjects) is not 0:
                    self._logic._createPair(self.line_mode_beg, mobjects[0][1])
                    
                sheet = self._logic._getSheet()
                render_engine.SceneNode.removeChild(sheet.sceneNodeChilds, self.line_mode_line.sceneNode)
                self.line_mode_line.setBegin(None)
                self.line_mode_beg = None
                self.state = SCgEditMode.ES_None
                    
                return True
        elif _id == ois.MB_Middle:
            if self.state == SCgEditMode.ES_None:
                self.state = SCgEditMode.ES_Translate
                render_engine.Gui.setPointer("hand")
                return True
        
        if self._logic._getSheet().haveSelected() and self.state is SCgEditMode.ES_None:
            # removing selection from all nodes
            self._logic._getSheet().unselectAll()
            return True
        
            
        return False
    
    def _onMouseReleased(self, _evt, _id):
        """Mouse button released event
        """
        # getting objects under mouse
        mobjects = self._logic._getSheet()._getObjectsUnderMouse(True)
        
        # * if released left button and node moving, then
        # stopping movement 
        if _id == ois.MB_Left:
            
            # check state
            if self.state is SCgEditMode.ES_Move:
                self.state = SCgEditMode.ES_None
                render_engine._gui_ignore_input_proc_result = False
                del self.move_obj
                return True
            
                
        elif _id == ois.MB_Right:
            pass
        
        elif _id == ois.MB_Middle:
            # translation
            if self.state is SCgEditMode.ES_Translate:
                self.state = SCgEditMode.ES_None
                render_engine.Gui.setPointer("arrow")
                return True
        
        return False
    
    def _onKeyPressed(self, _evt):
        """Key pressed event
        """
        BaseEditMode._onKeyPressed(self, _evt)
        
        key = _evt.key
        
        if key == ois.KC_LSHIFT:
            self._shift = True
                    
        elif key == ois.KC_T:
            self._handlerChangeType()
           
        elif key == ois.KC_SPACE:
            layout_group = self._logic._getSheet().getLayoutGroup()
            if layout_group is not None:
                if layout_group.isPlaying():
                    layout_group.stop()
                else:
                    layout_group.play()
                    
        elif _evt.key == ois.KC_F9:
            if render_engine.viewMode is render_engine.Mode_Isometric:
                self._logic._getSheet().changeMode(render_engine.Mode_Perspective)
            else:
                self._logic._getSheet().changeMode(render_engine.Mode_Isometric)
            self.line_mode_line._needModeUpdate()
                    
        elif key == ois.KC_F:
            # make selected sheet as root
            if self.state == SCgEditMode.ES_None:
                sheet = self._logic._getSheet()
                objs = sheet.getSelected()
                # getting object for making root
                if len(objs) == 1:
                    obj = objs[0]
                    if type(obj) == objects.ObjectSheet:
                        render_engine._kernel.setRootSheet(obj)
        elif key == ois.KC_ESCAPE:
            # revert state to default
            self.revertState()
            
        elif key == ois.KC_K:
            self._logic._createContour([ogre.Vector3(-3, -2, 0),
                                        ogre.Vector3(0, -3, 0),
                                        ogre.Vector3(3, -1, 0),
                                        ogre.Vector3(-3, 2, 0)
                                        ])
        
        return False
    
    def _onKeyReleased(self, _evt):
        """Key released event
        """
        BaseEditMode._onKeyReleased(self, _evt)
        
        key = _evt.key
        
        if key == ois.KC_LSHIFT:
            self._shift = False
               
        return False
    
    def _updateLineCreationObjects(self):
        """Call updates for objects that draws in line creation mode
        """
        self.line_mode_obj.needUpdate = True
        self.line_mode_obj._update(0)
        self.line_mode_line.needUpdate = True
        self.line_mode_line._update(0)
        
    def revertState(self):
        
        if self.state == SCgEditMode.ES_LineCreate:
            sheet = self._logic._getSheet()
            render_engine.SceneNode.removeChild(sheet.sceneNodeChilds, self.line_mode_line.sceneNode)
            self.line_mode_line.setBegin(None)
            self.line_mode_beg = None
        
        
        self.state = SCgEditMode.ES_None
            
    def _onToolBarButtonPush(self, button):
        
        data = button.getUserData()
        for idx in xrange(self.EM_Count):
            if idx == data:
                self.toolbar[idx].setChecked(True)
            else:
                self.toolbar[idx].setChecked(False)
        
    ################
    ### handlers ###
    ################
    def _handlerChangeType(self, _item = None):
        """Handler for change type event
        """
        # change type of selected element
        if self.state == SCgEditMode.ES_None:
            sheet = self._logic._getSheet()
            objs = sheet.getSelected()
            # get object for type changing 
            if len(objs) == 1:
                self._changeType(objs[0])
                
    def _handlerChangeIdtf(self, _item = None):
        """Handler for change idtf event
        """
        self._setIdtf()
      
    def _handlerSelChanged(self):
        """Handler for selection changed event
        """
        self._updateVisualMenu()
        
    def _handlerChangeContent(self, _item = None):
        """Handler for changing content
        """
        if self.state == SCgEditMode.ES_None:
            sheet = self._logic._getSheet()
            objs = sheet.getSelected()
            if len(objs) == 1 and type(objs[0]) is scg_objects.SCgNode:
                self._changeContent(objs[0])
                
    def _handlerContentShow(self, _item = None):
        if self.state == SCgEditMode.ES_None:
            sheet = self._logic._getSheet()
            objs = sheet.getSelected()
            if len(objs) == 1 and isinstance(objs[0], objects.ObjectSheet):
                objs[0].showContent()
                self._updateVisualMenu()
    
    def _handlerContentHide(self, _item = None):
        if self.state == SCgEditMode.ES_None:
            sheet = self._logic._getSheet()
            objs = sheet.getSelected()
            if len(objs) == 1 and isinstance(objs[0], objects.ObjectSheet):
                objs[0].hideContent()
                self._updateVisualMenu()
      
    def _dialog_del_callback(self):
        self.state = SCgEditMode.ES_None
        self.dialog = None
      
    #############
    ### Types ###
    #############
    def _changeType(self, _obj):
        """Creates control to change object type
        
        @param _obj: object to change type
        @type _obj: objects.ObjectDepth  
        """
        self.state = SCgEditMode.ES_TypeChange
        self.dialog = scg_controls.TypeChanger(_obj, self._dialog_del_callback)
        self.dialog.run()
           
        #self.state = SCgEditMode.ES_None
        
    ################
    ### Contents ###
    ################
    def _changeContent(self, _node):
        """Changes content type for a specified node
        @param _node:    node to change content type
        @type _node:    SCgNode
        """
        self.state = SCgEditMode.ES_ContType
        self.dialog = scg_controls.ContentChanger(_node, self._dialog_del_callback)
        self.dialog.run()
#        self._create_content_combo()
#        pos = render_engine.pos3dTo2dWindow(_node.getPosition() + _node.getScale() / 2)
#        
#        if pos is not None:
#            self.content_combo.setPosition(pos[0], pos[1])
#            self.object_active = _node
#            self.content_combo.subscribeEventAccept(self, "_contentAccept")
#            
#            # getting available for editing formats
#            session = render_engine._kernel.session()
#            self.fmts = render_engine._kernel.getRegisteredEditorFormats()
#            for fmt in self.fmts:
#                self.content_combo.addItem(unicode("#ffffff%s" % (session.get_idtf(fmt))))
#            
#        else:
#            self._destroy_content_combo()
        
    def _contentAccept(self, _widget, _v):
        """Handler for content combo accept
        """
        fmt = self.fmts[_v]
        
        assert type(self.object_active) is scg_objects.SCgNode
        window = scg_utils.createWindowFromNode(self.object_active, fmt)
        
        self._logic._getSheet().unselectAll()
        self._logic._getSheet().select(window)
    
        self._destroy_content_combo()
        self.state = SCgEditMode.ES_None
        self.object_active = None        
        del self.fmts
    
    
    ###################
    ### Visual menu ###
    ###################
    def _createVisualMenu(self):
        """Creates visual menu
        """
        self.vis_menu = VisualMenu()
        
        # identificator changing
        self.mi_idtf = VisualMenuItem()
        self.mi_idtf.callback = self._handlerChangeIdtf
        self.mi_idtf.setText("Change identifier")
        self.vis_menu.appendItem(self.mi_idtf)
        
        # type changing
        self.mi_type = VisualMenuItem()
        self.mi_type.callback = self._handlerChangeType
        self.mi_type.setText("Change type")
        self.vis_menu.appendItem(self.mi_type)
        
        # content changing
        self.mi_contentChange = VisualMenuItem()
        self.mi_contentChange.callback = self._handlerChangeContent
        self.mi_contentChange.setText("Change content")
        self.vis_menu.appendItem(self.mi_contentChange)
        
        # content showing
        self.mi_content_show = VisualMenuItem()
        self.mi_content_show.callback = self._handlerContentShow
        self.mi_content_show.setText("Show content")
        self.vis_menu.appendItem(self.mi_content_show)
        
        # content hiding
        self.mi_content_hide = VisualMenuItem()
        self.mi_content_hide.callback = self._handlerContentHide
        self.mi_content_hide.setText("Hide content")
        self.vis_menu.appendItem(self.mi_content_hide)
        
    def _updateVisualMenu(self):
        """Updates visual menu depending on selection
        """
        if self._logic is None or self._logic._getSheet() is None:
            return
        
        import types
        sel_objects = [] + self._logic._getSheet().getSelected()
        
        if self.vis_menu.isShow():
            self.vis_menu.hide()
        
        if not self.active: return
        
        n = len(sel_objects)
        if n == 1:
            obj = sel_objects[0]
            
            # check types
            isNode = isinstance(obj, scg_objects.SCgNode)
            isPair = isinstance(obj, scg_objects.SCgPair)
            isContent = isinstance(obj, objects.ObjectSheet) 
            
            # change type
            self.mi_type.setEnabled(isNode or isPair)
            # content
            self.mi_contentChange.setEnabled(isNode)
            # idtf
            self.mi_idtf.setEnabled(obj._getScAddr() is None)
            
            cs = ch = False
            if isContent:
                cs = not obj.isContentShow
                ch = obj.isContentShow
                
            self.mi_content_show.setEnabled(cs)
            self.mi_content_hide.setEnabled(ch)
        else:
            self.mi_type.setEnabled(False)
            self.mi_contentChange.setEnabled(False)
            self.mi_idtf.setEnabled(False)
            self.mi_content_show.setEnabled(False)
            self.mi_content_hide.setEnabled(False)
            
        if n > 0:   self.vis_menu.show(render_engine.pos3dTo2dWindow(sel_objects[0].getPosition()))
        
