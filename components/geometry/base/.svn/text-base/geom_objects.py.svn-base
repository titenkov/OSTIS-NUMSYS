
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
Created on 24.11.2009

@author: Denis Koronchick
'''

import suit.core.objects
import suit.core.exceptions
import suit.core.render.engine as render_engine
import geom_env
import math
import ogre.renderer.OGRE as ogre

state_post = {suit.core.objects.Object.OS_Normal: 'Normal',
              suit.core.objects.Object.OS_Selected: 'Selected',
              suit.core.objects.Object.OS_Highlighted: 'Highlighted'}
    
class GeometryPoint(suit.core.objects.ObjectDepth):
    """Object that represents geometry point
    
    @warning: creation of this object need be synchronized
    """
    def __init__(self):
        suit.core.objects.ObjectDepth.__init__(self, None)
        
        # creating entity
        self.entity = render_engine.SceneManager.createEntity("GeometryPoint_" + str(self), geom_env.mesh_point)
        self.sceneNode.attachObject(self.entity)
        self.setScale(ogre.Vector3(0.7, 0.7, 0.7))
            
    
    def __del__(self):
        suit.core.objects.ObjectDepth.__del__(self)
        
    def delete(self):
        render_engine.SceneManager.destroyEntity(self.entity)
        suit.core.objects.ObjectDepth.delete(self)
        
    def _getMaterialName(self):
        """Return material name for point object based on current state
        
        @return: material name
        @rtype: str
        """
        return geom_env.material_state_pat % ("point_%s" % (state_post[self.getState()]))
        
    def _updateView(self):
        """View update function
        
        Updates state for object
        """
        if self.needStateUpdate:
            self.needStateUpdate = False
            self.entity.setMaterialName(self._getMaterialName())
            
        suit.core.objects.ObjectDepth._updateView(self)
        
    def get_idtf(self):
        """Returns object identificator.
        It parse structures like: Point(A), Point A, pA and return A
        """
        #FIXME:    add parsing for Point(A), Point A and etc. structures
        idtf = self.getText()
        if idtf is None or len(idtf) == 0:
            idtf = str(self)[-9:-2] # FIXME:    make identification more useful
            
        return idtf
        
    def build_text_idtf(self):
        """Builds text identificator for an object
        """        
        return "%s(%s)" % (u'Точка',
                           self.get_idtf())

    def build_simple_text_idtf(self):
        """Returns simple identificator.
        For example: for Point(A) it builds pA
        """
        #FIXME:    add parsing for Point(A), Point A and etc. structures
        return "%s%s" % (u'т', self.get_idtf())
        
    
class GeometryLineSection(suit.core.objects.ObjectLine):
    """Object that represents geometry line section
    """
    def __init__(self):
        suit.core.objects.ObjectLine.__init__(self, None)
        
        # creating entity
        self.entity = render_engine.SceneManager.createEntity("geom_lsection_%s" % str(self), geom_env.mesh_lsect)
        self.sceneNode.attachObject(self.entity)
        self.radius = 0.1
        
        # need to be moved into base class GeometryProperty in future
        self.length = None
        self.length_text_obj = None
        
        self.needLengthUpdate = False
        self.needLengthPositionUpdate = False
                
    def __del__(self):
        suit.core.objects.ObjectLine.__del__(self)
    
    def delete(self):
        """Object deletion
        """
        if self.entity:
            render_engine.SceneManager.destroyEntity(self.entity)
        
        if self.length_text_obj is not None:
            self.length_text_obj.delete() 
            self.length_text_obj = None
        
        suit.core.objects.ObjectDepth.delete(self)
        
    def _getMaterialName(self):
        """Returns material name based on object state
        """
        
        return geom_env.material_state_pat % ("lsec_%s" % (state_post[self.getState()]))
    
    def setLength(self, _length):
        self.length = _length
        self.needLengthUpdate = True
        self.needViewUpdate = True
        
    def getLength(self):
        return self.length
        
    def _update(self, _timeSinceLastFrame):
        
        # updating geometry
        if self.needUpdate:
            # notify, that need to update length position
            self.needLengthPositionUpdate = True
            
            # calculate rotation
            op1 = self.beginObject.getPosition()
            op2 = self.endObject.getPosition()
        
            p1 = self.beginObject._getCross(op2)
            p2 = self.endObject._getCross(op1)
            
            self.begin_pos = p1
            self.end_pos = p2
            
            # rotating and scaling line
            orientV = p2 - p1
            self.sceneNode.setPosition(p1)
            l = orientV.length()
            if l < 0.1:
                self.sceneNode.setDirection(ogre.Vector3(1, 1, 0), ogre.SceneNode.TS_PARENT, [0, 1, 0])
            else:
                self.sceneNode.setDirection(orientV, ogre.SceneNode.TS_PARENT, [0, 1, 0])
            self.sceneNode.setScale(ogre.Vector3(self.radius * 2, l, self.radius * 2))
            
            # update identificator position
            if self.begin_pos and self.end_pos and self.text_obj:
                self.text_obj.setPosition((self.begin_pos + self.end_pos) / 2.0 + self.radius * 1.2 * ogre.Vector3(1.0, 1.0, 0.0))
                self.needUpdate = False
            else:
                self.needUpdate = True
            
        if self.length_text_obj is not None: self.length_text_obj._update(_timeSinceLastFrame)
        
        suit.core.objects.ObjectLine._update(self, _timeSinceLastFrame)
        
    def _updateView(self):
        """View update function
        
        Updates state for object
        """
        if self.needStateUpdate:
            self.needStateUpdate = False
            self.entity.setMaterialName(self._getMaterialName())
            
        if self.needLengthUpdate or self.needSceneAttachUpdate:
            self.needLengthUpdate = False
            self.needSceneAttachUpdate = False
            self._updateLength()
            
        if self.needLengthPositionUpdate:
            self.needLengthPositionUpdate = False
            self._updateLengthPosition()
            
        suit.core.objects.ObjectDepth._updateView(self)
        
    def _updateLength(self):
        """Updates length object
        """
        if self.length is not None and self.isSceneAttached:                
            if not self.length_text_obj:
                self.length_text_obj = suit.core.objects.ObjectText(self.getPosition(), self)
                self.length_text_obj.show()
                
            self.length_text_obj.setText("#000000%s" % str(self.length))
        else:
            self.length_text_obj = None
            
        self.needLengthPositionUpdate = True
        self.needViewUpdate = True
            
    def _updateLengthPosition(self):
        """Recalculate length text position 
        """
        if self.length_text_obj:
            
            # get center
            p1 = self.getBegin().getPosition()
            p2 = self.getEnd().getPosition()
            
            pm = p1.midPoint(p2)
            
            angle = math.atan2(p2.y - p1.y, p2.x - p1.x)
            angle = ogre.Radian(angle) + ogre.Degree(90.0).valueRadians()
            angle = angle.valueRadians()
           
            r = 0.2
            self.length_text_obj.setPosition(ogre.Vector3(r * math.cos(angle), r * math.sin(angle), 0.0) + pm) 
     
    def get_idtf(self):
        """Returns object identificator.
        It parse structures like: Point(A), Point A, pA and return A
        """
        #FIXME:    add parsing for Point(A), Point A and etc. structures
        idtf = self.getText()
        if idtf is None or len(idtf) == 0:
            return None
            
        return idtf
     
    def build_text_idtf(self):
        """Builds text identificator for an object
        """
        idtf = self.get_idtf()
        if not idtf:
            return "%s(%s,,%s)" % (u'Отрезок',
                                   self.beginObject.build_simple_text_idtf(),
                                   self.endObject.build_simple_text_idtf())
        else:
            return "%s(%s)" % (u'Отрезок', idtf)

    def build_simple_text_idtf(self):
        """Returns simple identificator.
        For example: for Point(A) it builds pA
        """
        #FIXME:    add parsing for Point(A), Point A and etc. structures
        return self.build_text_idtf()
     
class GeometryCircle(suit.core.objects.ObjectDepth):
    
    def __init__(self):
        suit.core.objects.ObjectDepth.__init__(self)
        
        self.width = 0.2
        self.radius = 1.0
        self.sectors = 90
        
        self.manualObject = None
        self.center_point = None
        
        self.needMeshUpdate = False
        self.needCenterPointUpdate = False
        
    def __del__(self):
        suit.core.objects.ObjectDepth.__del__(self)
        
    def delete(self):
            
        if self.center_point is not None:
            self.center_point.removeLinkedObject(suit.core.objects.Object.LS_OTHER, self)
            self.center_point = None
            
        render_engine.SceneManager.destroyManualObject(self.manualObject)
        suit.core.objects.ObjectDepth.delete(self)
        
    def _getMaterialName(self):
        """Returns material name based on object state
        """
        
        return geom_env.material_state_pat % ("lsec_%s" % (state_post[self.getState()]))
        
    def _update(self, _timeSinceLastFrame):
        
        if not self.needUpdate:
            return
        
        suit.core.objects.ObjectDepth._update(self, _timeSinceLastFrame)
        
        # update circle position based on center point
        self.setPosition(self.center_point.getPosition())
        
        if self.needMeshUpdate:
            self._updateMesh()
            self.needMeshUpdate = False
        
    def _updateView(self):
                
        if self.needCenterPointUpdate:
            self.needCenterPointUpdate = False
            
        if self.needStateUpdate:
            self.needStateUpdate = False
            self.manualObject.setMaterialName(0, self._getMaterialName())
            
        suit.core.objects.ObjectDepth._updateView(self)
        
        
    def _updateMesh(self):
        """Updates circle mesh
        """
        # recreate geometry
        if self.manualObject is None:
            #sceneMngr.destroyManualObject(self.__manualObject)
            self.manualObject = render_engine._ogreSceneManager.createManualObject(str(self))
            self.manualObject.setDynamic(True)
            # attach to scene node
            self.sceneNode.attachObject(self.manualObject)
            self.manualObject.begin(self._getMaterialName())
        else:
            self.manualObject.beginUpdate(0)
            
        # recalculate mesh
        a_step = ogre.Degree(360 / self.sectors).valueRadians()
        angle = 0.0
        r_in = self.radius - self.width / 2.0
        r_out = r_in + self.width
        for sector in xrange(self.sectors):
            vx = math.cos(angle)
            vy = math.sin(angle)
            
            self.manualObject.position(vx * r_in, vy * r_in, 0.0)
            self.manualObject.normal(0, 0, 1)
            self.manualObject.position(vx * r_out, vy * r_out, 0.0)
            self.manualObject.normal(0, 0, 1)
            
            angle += a_step
            
        for idx in xrange(self.sectors):
            idx1 = idx * 2
            self.manualObject.quad(idx1, idx1 + 1, idx1 + 3, idx1 + 2)
        self.manualObject.quad(self.sectors*2 - 2, self.sectors*2 - 1, 1, 0)
        self.manualObject.end()
        
    def setRadius(self, _radius):
        """Set circle radius
        @param _radius: radius length
        @type _radius: float
        """
        self.radius = _radius
        self.needMeshUpdate = True
        
    def setCenterPoint(self, _point):
        """Sets center point object
        @param _point: center point object
        @type _point: GeometryPoint
        """
        if self.center_point is not None:
            self.center_point.removeLinkedObject(suit.core.objects.Object.LS_OTHER, self)
        
        self.center_point = _point
        self.needCenterPointUpdate = True
        self.needViewUpdate = True
        
        if self.center_point is not None:
            self.center_point.addLinkedObject(suit.core.objects.Object.LS_OTHER, self)
            
    def _checkRayIntersect(self, ray):
        """Check if ray intersects union object.
        Just check if it intersects any of object included to union.
        
        @param ray:    ray for intersection checking
        @type ray:    ogre.Ray
        """
        res, pos = suit.core.objects.ObjectDepth._checkRayIntersect(self, ray)
        if not res:
            return False, -1 
        
        # works just for a isometric mode
        m = ogre.Matrix4() 
        self.getSceneNode().getWorldTransforms(m)
        p = ogre.Matrix4.getTrans(m)
        
        pl = ogre.Plane(ray.getDirection(), p)
        pr = ray.intersects(pl)
        if not pr.first:
            return False, -1
        
        d = ray.getPoint(pr.second)
        
        dist = self.center_point.getPosition().distance(d)
        if math.fabs(dist - self.radius) <= self.width / 2.0:
            return True, 0
        
        return False, -1
    
    def build_text_idtf(self):
        """Builds text identificator for an object
        """
        idtf = self.get_idtf()
        if not idtf:
            return "%s(%s)" % (u'Окружность',
                                   self.center_point.build_simple_text_idtf())
        else:
            return "%s(%s)" % (u'Окружность', idtf)

    def build_simple_text_idtf(self):
        """Returns simple identificator.
        For example: for Point(A) it builds pA
        """
        #FIXME:    add parsing for Point(A), Point A and etc. structures
        return self.build_text_idtf()
    
class GeometryTriangle(suit.core.objects.ObjectDepth):
    
    def __init__(self, _objects):
        """Constructor
        
        @param _line: list of Geometry objects, that would be used to construct triangle
        @type _line: list
        """
        suit.core.objects.ObjectDepth.__init__(self)
        
        self.__manualObject = None  # manual object to store and render geometry
        self.objects = _objects
        self.points = []        # triangle vertex points
        
        self.buildTriangle()    # build triangle based on objects
    
    def __del__(self):
        suit.core.objects.ObjectDepth.__del__(self)
    
    def delete(self):
        """Object deletion
        """
        for obj in self.objects:
            obj.removeLinkedObject(suit.core.objects.Object.LS_OTHER, self)
        
        if self.__manualObject:
            render_engine.SceneManager.destroyManualObject(self.__manualObject)
            
        suit.core.objects.ObjectDepth.delete(self)
        
    def _getMaterialName(self):
        """Returns material name based on object state
        """        
        return geom_env.material_state_pat % ("triangle_%s" % (state_post[self.getState()]))
    
    def _update(self, _timeSinceLastFrame):
        """Object update
        """
        
        if self.needUpdate:
            # notify, that text position need to be updated
            self.needTextPositionUpdate = True
            
            # calculate center position
            p1 = self.points[0].getPosition()
            p2 = self.points[1].getPosition()
            p3 = self.points[2].getPosition()
            
            s1 = p1.distance(p2)
            s2 = p2.distance(p3)
            s3 = p3.distance(p1)
            
            perim = 1 / (s1 + s2 + s3)
            
            # using Geron S=UR
            x = (s2 * p1.x + s3 * p2.x + s1 * p3.x) * perim
            y = (s2 * p1.y + s3 * p2.y + s1 * p3.y) * perim
            
            self.position = ogre.Vector3(x, y, 0)
            self.sceneNode.setPosition(self.position)
            
            # update/create mesh
            if self.__manualObject is None:
                self.__manualObject = render_engine._ogreSceneManager.createManualObject(str(self))
                self.__manualObject.setDynamic(True)
                self.sceneNode.attachObject(self.__manualObject)
                self.__manualObject.begin(self._getMaterialName())
            else:
                self.__manualObject.beginUpdate(0)
                
            for point in self.points:
                self.__manualObject.position(point.getPosition() - self.position)
                self.__manualObject.normal(0, 0, 1)
            
            self.__manualObject.triangle(2, 1, 0)
            
            self.__manualObject.end()
        
        suit.core.objects.ObjectDepth._update(self, _timeSinceLastFrame)
        
    def _updateView(self):
        """View update function
        
        Updates state for object
        """
        if self.needStateUpdate:
            self.needStateUpdate = False
            self.__manualObject.setMaterialName(0, self._getMaterialName())
             
        suit.core.objects.ObjectDepth._updateView(self)
    
    def _checkRayIntersect(self, ray):
        """Check if ray intersects union object.
        Just check if it intersects any of object included to union.
        
        @param ray:    ray for intersection checking
        @type ray:    ogre.Ray
        """
        res = suit.core.objects.ObjectDepth._checkRayIntersect(self, ray)
        if not res[0]:
            return res
        
        res = ogre.Math.intersects(ray,
                                    self.points[0].getPosition(),
                                    self.points[1].getPosition(),
                                    self.points[2].getPosition())
        
        return res.first, res.second
    
    
    def buildTriangle(self):
        """Builds triangle based on objects list
        """
        
        if len(self.objects) == 3:
            # fist way to build triangle based on lines
            lines3 = True
            for obj in self.objects:
                if not isinstance(obj, GeometryLineSection):
                    lines3 = False
                    
            if lines3:
                point_pairs = []
                for line in self.objects:
                    point_pairs.append( (line.getEnd(), line.getBegin()) )
                    
                # trying to find lines order
                point_pairs_sorted = [point_pairs[0]]
                if point_pairs[1][0] == point_pairs[0][1]:
                    point_pairs_sorted.append(point_pairs[1])
                    point_pairs_sorted.append(point_pairs[2])
                else:
                    point_pairs_sorted.append(point_pairs[2])
                    point_pairs_sorted.append(point_pairs[1])
                    
                point_pairs = point_pairs_sorted
                # check if lines connected
                connected = True
                if not point_pairs[0][1] == point_pairs[1][0]:
                    connected = False
                elif not point_pairs[1][1] == point_pairs[2][0]:
                    connected = False
                elif not point_pairs[2][1] == point_pairs[0][0]:
                    connected = False
                
                if connected:
                    for pt in point_pairs:
                        self.points.append(pt[0])
        
        # link to objects for update
        for obj in self.objects:
            obj.addLinkedObject(suit.core.objects.Object.LS_OTHER, self)
    
     
class GeometryUnion(suit.core.objects.ObjectDepth):
    """Object that represents objects union.
    
    It can consist of any count of objects.
    """
    
    def __init__(self):
        suit.core.objects.ObjectDepth.__init__(self)
        
        self.objects = []
        
    def __del__(self):
        suit.core.objects.ObjectDepth.__del__(self)
        
    def _checkRayIntersect(self, ray):
        """Check if ray intersects union object.
        Just check if it intersects any of object included to union.
        
        @param ray:    ray for intersection checking
        @type ray:    ogre.Ray
        """
        for obj in self.objects:
            res = obj._checkRayIntersect(ray)
            if res[0]: 
                return res
        
        return False, -1
    
    
    def appendObject(self, _obj):
        """Appends object to union
        @param _obj:    object to append
        @type _obj:    suit.core.objects.ObjectDepth
        """
        if not isinstance(_obj, suit.core.objects.ObjectDepth):
            raise TypeError("Unsupported type of object '%s' in union '%s'" % (str(_obj), str(self)))
        
        if _obj in self.objects:
            raise suit.core.exceptions.ItemAlreadyExistsError("Object '%s' already exists in union '%s'" % (str(_obj), str(self)))
        
        self.objects.append(_obj)
        
    def removeObject(self, _obj):
        """Removes object from union
        @param _obj:    object for removing
        @type _obj:    suit.core.objects.ObjectDepth
        """
        pass