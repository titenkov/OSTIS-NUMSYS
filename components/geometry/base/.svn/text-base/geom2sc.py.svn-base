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
Created on 01.02.2010

@author: Denis Koronchik
'''

from suit.core.objects import Translator
import suit.core.sc_utils as sc_utils
import suit.core.objects as objects
import suit.core.kernel as core
import sc_core.pm as sc
import geom_keynodes
import geom_objects
import geom_env as env
import suit.core.keynodes as keynodes


def get_sc_element(_segment, _idtf, _object, _sc_type):
    """Generates scs-element, that represent geometry object
    @param _segment:    segment to work with data in sc-memory
    @type _segment:    sc_segment
    @param _idtf:    identificator for search
    @type _idtf:    str
    @param _object:    object to create sc-element for
    @type _object:    Object
    @param _sc_type:    sc-type for element
    @type _sc_type:    sc_type
    
    @return: addr of create sc-element
    @rtype: sc_global_addr
    """
    session = core.Kernel.session()
    
    # getting node idtf
    
    
    sc_object = None
    el = None
    isUri = False
    
    # if idtf empty, then creating new element
    if _idtf is None:
        el = session.create_el(_segment, sc_type)
    else:
        # check if idtf if full uri
        isUri = _idtf.startswith('/')
    
    # trying to find object by idtf, if it doesn't exists, then creating it
    try:
        if el is None:
           
            
            if isUri:
                el = session.find_el_full_uri(_idtf)
                if el is None:
                    el = session.create_el_full_uri(_idtf, _sc_type)[1]
            else:
                _segs = [_segment.get_full_uri()]
                _segs.extend(env.search_segments)
                # trying to find element
                el = sc_utils.getElementByIdtf(_idtf, _segs)
                if el is None:
                    el = session.create_el_idtf(_segment, _sc_type, _idtf)[1]
    except:
        import sys, traceback
        print sys.exc_info()[0]
        traceback.print_exc(file=sys.stdout)
        return None
    
    _object._setScAddr(el)
    
    return el

def translate_point(_segment, _object, _params):
    """Translates point object to sc-memory
    """
    idtf = _object.getText()
    # encode idtf to cp1251
    idtf = sc_utils.utf8ToCp1251(str(idtf))
    
    # FIXME:    make tool for idtf normalization
    idtf = u"Точка(%s)" % idtf
    
    _addr = get_sc_element(_segment, idtf, _object, sc.SC_N_CONST)
    
    # include sc-element to points
    session = core.Kernel.session()
    sc_utils.createPairPosPerm(session, _segment, geom_keynodes.Objects.point, _addr, sc.SC_CONST)
    
    if not sc_utils.checkIncToSets(session, _addr, [keynodes.info.stype_ext_obj_abstract], sc.SC_A_CONST | sc.SC_POS | sc.SC_PERMANENT):
        sc_utils.createPairPosPerm(session, _segment, keynodes.info.stype_ext_obj_abstract, _addr, sc.SC_CONST)
    
    return True

def translate_line_sec(_segment, _object, _params):
    """Translates line section to sc-memory
    """
    idtf = _object.getText()
    if idtf is not None:
        # encode idtf to cp1251
        idtf = sc_utils.utf8ToCp1251(str(idtf))
        
        if len(idtf) > 0:
            idtf = u"Отрезок (%s)" % idtf
    else:
        idtf_beg = _object.getBegin().getText()
        idtf_end = _object.getEnd().getText()
        
        if idtf_beg and idtf_end:
            idtf_beg = sc_utils.utf8ToCp1251(str(idtf_beg))
            idtf_end = sc_utils.utf8ToCp1251(str(idtf_end))
            
            if len(idtf_beg) > 0 and len(idtf_end) > 0:
                idtf = u"Отрезок (%s,,%s)" % (idtf_beg, idtf_end)
    
    _addr = None
    if idtf:    _addr = get_sc_element(_segment, idtf, _object, sc.SC_N_CONST)
    session = core.Kernel.session()
    if not _addr:   
        _addr = sc_utils.createNodeStruct(session, _segment, sc.SC_CONST)
        _object._setScAddr(_addr)
    sc_utils.createPairPosPerm(session, _segment, geom_keynodes.Objects.line_sector, _addr, sc.SC_CONST)
    
    if not sc_utils.checkIncToSets(session, _addr, [keynodes.info.stype_struct], sc.SC_A_CONST | sc.SC_POS):
        sc_utils.createPairPosPerm(session, _segment, keynodes.info.stype_struct, _addr, sc.SC_CONST)
    
    # end begin points
    addr_begin = _object.getBegin()._getScAddr()
    addr_end = _object.getEnd()._getScAddr()
    
    assert addr_begin and addr_end
    
    a1 = sc_utils.createPairBinaryOrient(session, _segment, _addr, addr_begin, sc.SC_CONST)
    sc_utils.createPairPosPerm(session, _segment, geom_keynodes.Relation.nrel_border_point, a1, sc.SC_CONST)
    a2 = sc_utils.createPairBinaryOrient(session, _segment, _addr, addr_end, sc.SC_CONST)
    sc_utils.createPairPosPerm(session, _segment, geom_keynodes.Relation.nrel_border_point, a2, sc.SC_CONST)
    
    # check if line have length and build it value
        # set value if it exists
    if _object.getLength() is not None:
        len_node = sc_utils.createNodeElement(session, _segment, sc.SC_CONST)
        sheaf = sc_utils.createPairBinaryOrient(session, _segment, _addr, len_node, sc.SC_CONST)
        sc_utils.createPairPosPerm(session, _segment, geom_keynodes.Relation.nrel_length, sheaf, sc.SC_CONST)
        
        len_val_node = sc_utils.createNodeElement(session, _segment, sc.SC_CONST)
        sheaf = sc_utils.createPairBinaryOrient(session, _segment, len_val_node, len_node, sc.SC_CONST)
        sc_utils.createPairPosPerm(session, _segment, keynodes.common.nrel_value, sheaf, sc.SC_CONST)
        
        len_val_cm_node = sc_utils.createNodeElement(session, _segment, sc.SC_CONST)
        a = sc_utils.createPairPosPerm(session, _segment, len_val_node, len_val_cm_node, sc.SC_CONST)
        sc_utils.createPairPosPerm(session, _segment, geom_keynodes.Relation.rrel_cm, a, sc.SC_CONST)
        
        idtf_node = sc_utils.createNodeSheaf(session, _segment, sc.SC_CONST)
        sheaf = sc_utils.createPairBinaryOrient(session, _segment, idtf_node, len_val_cm_node, sc.SC_CONST)
        sc_utils.createPairPosPerm(session, _segment, keynodes.common.nrel_identification, sheaf, sc.SC_CONST)
        
        dec_val_node = sc_utils.createNodeElement(session, _segment, sc.SC_CONST)
        session.set_content_real(dec_val_node, _object.getLength())
        a = sc_utils.createPairPosPerm(session, _segment, idtf_node, dec_val_node, sc.SC_CONST)
        sc_utils.createPairPosPerm(session, _segment, keynodes.common.rrel_dec_number, a, sc.SC_CONST)
    
def translate_circle(_segment, _object, _params):
    """Translates circle object to sc-memory
    """
    idtf = _object.getText()
    # encode idtf to cp1251
    idtf = sc_utils.utf8ToCp1251(str(idtf))
            
    # FIXME:    make tool for idtf normalization
    idtf = u"Окружность(%s)" % idtf
    
    _addr = get_sc_element(_segment, idtf, _object, sc.SC_N_CONST)
    
    # include sc-element to points
    session = core.Kernel.session()
    sc_utils.createPairPosPerm(session, _segment, geom_keynodes.Objects.circle, _addr, sc.SC_CONST)
    
    if not sc_utils.checkIncToSets(session, _addr, [keynodes.info.stype_ext_obj_abstract], sc.SC_A_CONST | sc.SC_POS | sc.SC_PERMANENT):
        sc_utils.createPairPosPerm(session, _segment, keynodes.info.stype_ext_obj_abstract, _addr, sc.SC_CONST)
        
    # add relation to center point
    addr_begin = _object.center_point._getScAddr()
    a1 = sc_utils.createPairBinaryOrient(session, _segment, _addr, addr_begin, sc.SC_CONST)
    sc_utils.createPairPosPerm(session, _segment, geom_keynodes.Relation.nrel_center, a1, sc.SC_CONST)
    
    return True

def translate_triangle(_segment, _object, _params):
    """Translates circle object to sc-memory
    """
    idtf = _object.getText()
    # encode idtf to cp1251
    idtf = sc_utils.utf8ToCp1251(str(idtf))
            
    # FIXME:    make tool for idtf normalization
    idtf = u"Треугольник(%s)" % idtf
    
    _addr = get_sc_element(_segment, idtf, _object, sc.SC_N_CONST)
    
    # include sc-element to points
    session = core.Kernel.session()
    sc_utils.createPairPosPerm(session, _segment, geom_keynodes.Objects.plane_triangle, _addr, sc.SC_CONST)
    
    if not sc_utils.checkIncToSets(session, _addr, [keynodes.info.stype_ext_obj_abstract], sc.SC_A_CONST | sc.SC_POS | sc.SC_PERMANENT):
        sc_utils.createPairPosPerm(session, _segment, keynodes.info.stype_ext_obj_abstract, _addr, sc.SC_CONST)
    
    # check if triangle based on line sectors
    lines = True
    for obj in _object.objects:
        if not isinstance(obj, geom_objects.GeometryLineSection):
            lines = False
            
    # add relation to sides
    if lines:
        for obj in _object.objects:
            sheaf = sc_utils.createPairBinaryOrient(session, _segment, _addr, obj._getScAddr(), sc.SC_CONST)
            sc_utils.createPairPosPerm(session, _segment, geom_keynodes.Relation.nrel_triangle_side, sheaf, sc.SC_CONST)
            
    # build square relation
    sq_node = sc_utils.createNodeElement(session, _segment, sc.SC_CONST)
    sheaf = sc_utils.createPairBinaryOrient(session, _segment, _addr, sq_node, sc.SC_CONST)
    sc_utils.createPairPosPerm(session, _segment, geom_keynodes.Relation.nrel_square, sheaf, sc.SC_CONST)
    
    return True

def translate_object(_segment, _object, _params):
    """Translates specified geometry object to SC-code.
    @param _segment:    segment to translate object in
    @type _segment:    sc_segment
    @param _object:    geometry object to translate
    @type _object:    SCgObject or SCgPair
    @param _params:    additional parameters to translate object. It contains list of sc-elements, that
    designates semantic types for specified object. sc-element, that designate translated object will be included to
    sets from _params
    @type _params:    list
    
    @return: if object translated successfully, then return True, else - False
    @rtype: bool
    """
    
    if isinstance(_object, geom_objects.GeometryPoint):
        return translate_point(_segment, _object, _params)
    elif isinstance(_object, geom_objects.GeometryLineSection):
        return translate_line_sec(_segment, _object, _params)
    elif isinstance(_object, geom_objects.GeometryCircle):
        return translate_circle(_segment, _object, _params)
    elif isinstance(object, geom_objects.GeometryTriangle):
        return translate_triangle(_Segment, _object, _params)
    else:
        return False
    
    return True

class TranslatorGeom2Sc(Translator):
    
    def __init__(self):
        Translator.__init__(self)
        
    def __del__(self):
        Translator.__del__(self)
        
    def translate_impl(self, _input, _output):
        """Translator implementation
        """
        # translating objects
        objs = objects.ScObject._sc2Objects(_input)
        
        assert len(objs) > 0
        sheet = objs[0]
        assert type(sheet) is objects.ObjectSheet
    
        segment = sheet.getTmpSegment()
    
        errors = []
        session = core.Kernel.session()
    
        # getting objects, that need to be translated
        trans_obj = []
        for obj in sheet.getChilds():
            _addr = obj._getScAddr()
            if _addr is None:
                trans_obj.append(obj)
                # remove old translation data
            else:
                if _addr.seg == segment:
                    session.erase_el(_addr)
                
        # make translation
        line_sec = []
        circles = []
        triangles = []
        for obj in trans_obj:
            print str(obj)
            # skipping lines for now
            if isinstance(obj, geom_objects.GeometryLineSection):
                line_sec.append(obj)
                continue
            elif isinstance(obj, geom_objects.GeometryCircle):
                circles.append(obj)
                continue
            elif isinstance(obj, geom_objects.GeometryTriangle):
                triangles.append(obj)
                continue
            
            if not translate_object(segment, obj, None):
                errors.append( ((obj, "Error while translate object %s" % str(obj))) )
            
        for obj in circles:
            if not translate_circle(segment, obj, None):
                errors.append( ((obj, "Error while translate object %s" % str(obj))) )
            
        for obj in line_sec:
            if not translate_line_sec(segment, obj, None):
                errors.append( ((obj, "Error while translate object %s" % str(obj))) )
                
        for obj in triangles:
            if not translate_triangle(segment, obj, None):
                errors.append( ((obj, "Error while translate object %s" % str(obj))) )

        return errors