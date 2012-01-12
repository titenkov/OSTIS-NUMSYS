
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
Created on 03.06.11
@author:  Zhitko V.A.
'''

import suit.core.keynodes as sc_key
import suit.core.kernel as core

from suit.core.objects import Factory

import sc_core.pm as pm

kernel = core.Kernel.getSingleton()
session = core.Kernel.session()

import sc2voice
import keynodes

_version_   =   "0.0.1"
_name_      =   "LUI Voice Output Manager"

import SSRLab.sui as SSRLab
import winTTS.winTTS as winTTS

modules = {
           "SSRLab":SSRLab,
           "winTTS":winTTS
           }

def initialize():
    print "[init] LUI Voice Output Manager"
    regTranslators()
    for key in modules.keys():
        regScWindows(key)
    return

def shutdown():
    print "[shutdown] LUI Voice Output Manager"
    return

def regScWindows(name):
    segment = session.open_segment(u"/ui/core")
    window = session.create_el(segment, pm.SC_N_CONST)
    sc_window = session.create_el_full_uri(u"/ui/core/%s" % name)
    if sc_window[0]:
        session.gen3_f_a_f(segment, keynodes.ui.voice, sc_window[1], pm.SC_A_CONST|pm.SC_POS|pm.SC_ACTUAL)
        session.gen3_f_a_f(segment, sc_key.ui.sc_window, sc_window[1], pm.SC_A_CONST|pm.SC_POS|pm.SC_ACTUAL)
    return sc_window[1]

def regTranslators():
    global sc2voice_factory
    sc2voice_factory = Factory(sc2voice_creator)
    kernel.registerTranslatorFactory(sc2voice_factory, [sc_key.ui.format_sc], [keynodes.ui.voice])
    return

def sc2voice_creator():
    return sc2voice.TranslatorSc2Voice(modules)