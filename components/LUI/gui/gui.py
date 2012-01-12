# -*- coding: utf-8 -*-
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
Created on 03.11.10
@author:  Zhitko V.A.
'''

import suit.core.render.mygui as mygui
import suit.core.render.engine as render_engine

class UI:
    
    def __init__(self, lui):
        print "[init] LUI GUI"
        self.lui = lui
        #global input 
        self.input = Input(lui.processQuestion,lui.processQuestion2Text)
        
    def setText(self, str):
        self.input.setText(str.decode('cp1251').encode('utf-8'))
    
class Input:
    def __init__(self,func,testFunc = None):
        self.window = None
        self.buttonOk = None
        self.edit = None
        self.vscrool = None
        
        self.window_h = 40
        self.window_w = 500
        
        self.button_h = 30
        self.button_w = 40
        
        self.createEls()
        self.func = func
        self.testFunc = testFunc
        
    def __del__(self):
        #self.destroyEls()
        pass

    def createEls(self):
        self.window = render_engine.Gui.createWidgetT(
                        "Window", "Panel", 
                        mygui.IntCoord(10,
                                       render_engine.Window.height - self.window_h - 60,
                                       self.window_w, 
                                       self.window_h),
                        mygui.Align())

        self.buttonOk = self.window.createWidgetT(
                        "Button", "Button",
                        mygui.IntCoord(self.window_w - self.button_w - 20 - 10, 
                                       5,
                                       self.button_w, 
                                       self.button_h),
                        mygui.Align())
        
        self.buttonHideShow = self.window.createWidgetT(
                        "Button", "Button",
                        mygui.IntCoord(self.window_w - 20 - 5, 
                                       5,
                                       20, 
                                       self.button_h),
                        mygui.Align())
        
        self.edit = self.window.createWidgetT(
                        "Edit", "Edit",
                        mygui.IntCoord(5, 
                                       5,
                                       self.window_w - self.button_w - 20 - 20, 
                                       self.button_h),
                        mygui.Align())
        
        self.window.setVisible(True)
        self.buttonOk.setVisible(True)
        self.buttonOk.setCaption("Ok")
        self.buttonHideShow.setVisible(True)
        self.buttonHideShow.setCaption("+")
        
        self.edit.setVisible(True)
        self.edit.setCaption("вывести полную семантическую окрестность понятия плоскость")
        #self.edit.setCaption("как выглядит тупоугольный треугольник")
        
        self.buttonOk.subscribeEventMouseButtonClick(self, "_buttonWndOutClick")
        self.buttonHideShow.subscribeEventMouseButtonClick(self, "_buttonShowHideClick")
        
    def _buttonWndOutClick(self, widget):
        text = self.edit.getCaption()
        self.func(text)
    
    def _buttonShowHideClick(self, widget):
        # TODO Hide/Show
        text = self.edit.getCaption()
        self.testFunc(text)
        
    def setText(self, str):
        self.edit.setCaption(str)
        
    def destroyEls(self):
        if self.buttonOk is not None:
            render_engine.Gui.destroyWidget(self.buttonOk)
            #self.buttonOk = None
            
        if self.edit is not None:
            render_engine.Gui.destroyWidget(self.edit)
            #self.edit = None
            
        if self.window is not None:
            render_engine.Gui.destroyWidget(self.window)
            #self.window = None