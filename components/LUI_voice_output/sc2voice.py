
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
Created on 03.06.2011

@author: Zhitko V.A.
'''

from suit.core.objects import Translator
import sc_core.pm as sc
import suit.core.kernel as sc_core

session = sc_core.Kernel.session()

class TranslatorSc2Voice(Translator):
    def __init__(self, modules):
        Translator.__init__(self)
        self.modules = modules
        
    def __del__(self):
        Translator.__del__(self)
        
    def translate_impl(self, _input = None, _output = None):
        """Translator implementation
        @param _input:    input data set
        @type _input:    sc_global_addr
        @param _output:    output window (must be created)
        @type _output:    sc_global_addr
        
        @return: list of errors each element of list is a tuple(object, error)
        @rtype: list
        """
        errors = []
        
        els = session.search3_f_a_a(_input, sc.SC_A_CONST|sc.SC_POS, sc.SC_NODE)
        expr = ""
        for el in els:
            expr = expr + session.get_content_str(el[2])
        
        name = session.get_idtf(_output)
        print "[Sc2Voice] Output by %s" % name
        module = self.modules[name]
        try:
            module.say(expr)
        except:
            print "[Sc2Voice] Error in %s" % name
            pass
        return errors