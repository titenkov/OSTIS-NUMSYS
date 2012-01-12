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

import parser.LsplParser as Lspl
import components.LUI.keynodes as keynodes

import sc_core.pm as sc
import sc_core.constants as sc_constants
import suit.core.kernel as sc_core
import suit.core.sc_utils as sc_utils
import suit.core.keynodes as sc_key


session = sc_core.Kernel.session()
session.open_segment(u"/etc/questions")
session.open_segment(u"/etc/com_keynodes")
session.open_segment(u"/seb/planimetry")
segment = sc_core.Kernel.segment()
        
import os
import sys

class core:
    def __init__(self, sc2text=None):
        print "[init] LUI core"
        self.sc2Text = sc2text
        self.parser = None
        self.lastQuestion = None
        try:
            self.loadParser()
        except:
            print "[fail] load LsplParser"
        self.loadPatterns()
        self.loadTargets()
        
    def loadParser(self):
        rml_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"parser")
        Lspl.setRMLpath(rml_dir)
        self.parser = Lspl.LsplParser()
        self.parser.loadMorphology()
        self.nsID = self.createNewNamespace()
        
    def loadTargets(self):
        self.targets = {}
        for key in keynodes.listOfObjects:
            it = session.create_iterator(session.sc_constraint_new(sc_constants.CONSTR_3_f_a_a,
                                                           key,
                                                           sc.SC_A_CONST | sc.SC_POS,
                                                           sc.SC_CONST | sc.SC_NODE
                                                           ), True)
            while not it.is_over():
                idtf = session.get_idtf(it.value(2))
                self.targets[idtf] = it.value(2)
                print "[Object basic] %s" % idtf
                syns = sc_utils.searchBinPairsAttrToNode(session,it.value(2),keynodes.nrel_identification,sc.SC_CONST)
                for syn in syns:
                    it2 = session.create_iterator(session.sc_constraint_new(sc_constants.CONSTR_3_f_a_a,
                                                           syn,
                                                           sc.SC_A_CONST | sc.SC_POS,
                                                           sc.SC_CONST | sc.SC_NODE
                                                           ), True)
                    while not it2.is_over():
                        idtf = session.get_content_str(it2.value(2))
                        if idtf is not None: self.targets[idtf] = it.value(2)
                        #print "[Object alter] %s" % idtf
                        it2.next()
                it.next()
        
    def loadPatterns(self):
        self.questionPatterns = {}
        it = session.create_iterator(session.sc_constraint_new(sc_constants.CONSTR_3_f_a_a,
                                                           keynodes.questions_types,
                                                           sc.SC_A_CONST | sc.SC_POS,
                                                           sc.SC_CONST | sc.SC_NODE
                                                           ), True)
        #questions = []
        print "[scan questions]"
        while not it.is_over():
            #questions.append(it.value(2))
            qIdtf = session.get_idtf(it.value(2))
            print "[scan] %s" % qIdtf
            syns = sc_utils.searchBinPairsAttrToNode(session,it.value(2),keynodes.nrel_identification,sc.SC_CONST)
            altqIdtf = None
            for syn in syns:
                it3 = session.create_iterator(session.sc_constraint_new(sc_constants.CONSTR_5_f_a_a_a_f,
                                                                        syn,
                                                                        sc.SC_A_CONST | sc.SC_POS,
                                                                        sc.SC_CONST | sc.SC_NODE,
                                                                        sc.SC_A_CONST | sc.SC_POS,
                                                                        keynodes.rrel_nl_idtf
                                                                        ), True)
                while not it3.is_over():
                    altqIdtf = session.get_content_str(it3.value(2))
                    it3.next()
            els = sc_utils.searchBinPairsAttrToNode(session,it.value(2),keynodes.nrel_pattern,sc.SC_CONST)
            for el in els:
                it2 = session.create_iterator(session.sc_constraint_new(sc_constants.CONSTR_3_f_a_a,
                                                           el,
                                                           sc.SC_A_CONST | sc.SC_POS,
                                                           sc.SC_CONST | sc.SC_NODE
                                                           ), True)
                while not it2.is_over():
                    if altqIdtf is None: altqIdtf = "XXX"
                    self.questionPatterns[altqIdtf] = it.value(2)
                    pattern = altqIdtf + " = " + session.get_content_str(it2.value(2))
                    self.addNewPattern(pattern)
                    it2.next()
            it.next()
        
    def addNewPattern(self, pattern, namespace = -1):
        if namespace is -1: namespace = self.nsID
        print "[register pattern] %s" % pattern
        self.parser.addPatternToNamespace(namespace, unicode(pattern).encode("CP1251"))
        
    def createNewNamespace(self):
        id = self.parser.createNewNamespace()
        self.addNewPattern("TARGET = {N}N", id)
        self.addNewPattern("TARGET = [A]N", id)
        return id
    
    def deleteNamespace(self, namespace = -1):
        if namespace is -1: namespace = self.nsID
        self.parser.eraseNamespace(namespace)
        
    def parseQuestion(self, question, namespace = -1):
        if namespace is -1: namespace = self.nsID
        res = self.parser.parseTextInNamespace(namespace, question)
        q = res.getQuestionVariants()
        o = res.getObjectsVariants()
        return (q, o)
    
    def processQuestion(self, text):
        print "[NL question] %s" % unicode(text)
        questions, targets = self.parseQuestion(unicode(text).encode("CP1251"))
        self.makeQuestion(questions, targets)
        
    def processQuestion2Text(self, text):
        print "[NL question to text] %s" % unicode(text)
        if self.lastQuestion is None: return
        answer = getAnswerByQuestion(self.lastQuestion)
        if answer is None: return
        answer = answer[0]
        text = u"Ответа нет"
        if answer:
            text = self.sc2Text(answer)
        out_string_to_user(text)
        
    def makeQuestion(self, listQuestions, listTargets):
        questions = []
        targets = []
        for question in listQuestions:
            if self.questionPatterns.has_key(question):
                print "[Question] = %s" % question
                questions.append(self.questionPatterns[question])
        for target in listTargets:
            if self.targets.has_key(target):
                print "[Object] = %s" % target
                targets.append(self.targets[target])
        if len(questions) is not 0 and len(targets) is not 0:
            self.lastQuestion = self.buidQuestion(questions, targets)
            print self.lastQuestion
        else:
            print "[Error] Bad NL question (q: %s, o: %s)" % (questions, targets)
    
    def buidQuestion(self, questionNode, objectsNodes):
        print "[Buid question]"
        return buildUserAtomQuestion(questionNode, objectsNodes)
        
def getAnswerByQuestion(sc_question):
    _a = sc.SC_A_CONST|sc.SC_POS
    answer_rel = session.search11_f_a_a_a_a_a_f_a_f_a_f(sc_question, _a, sc.SC_N_CONST, _a, sc.SC_N_CONST,
                                                         _a, sc_key.n_1, _a, sc_key.n_2, 
                                                         _a, sc_key.questions.nrel_answer)
    res = []
    if answer_rel is None: return None
    for ans in answer_rel:
        res.append(ans[4]) 
    if len(res) is 0: return None
    else: return res
    
def buildUserAtomQuestion(sc_qustions, sc_q_objects):
    # узел вопроса
    q_node = sc_utils.createNodeElement(session, segment, sc.SC_CONST)
    # добавляем во множество вопрос
    session.gen3_f_a_f(segment, sc_key.questions.question, q_node, sc.SC_A_CONST | sc.SC_POS)
    # добавляем во множество атомарный вопрос
    session.gen3_f_a_f(segment, sc_key.questions.atom, q_node, sc.SC_A_CONST | sc.SC_POS)
    # добавляем типы вопросов
    for sc_q in sc_qustions:
        session.gen3_f_a_f(segment, sc_q, q_node, sc.SC_A_CONST | sc.SC_POS)
    # добавляем объекты вопроса
    for sc_o in sc_q_objects:
        session.gen3_f_a_f(segment, q_node, sc_o, sc.SC_A_CONST | sc.SC_POS)
    # добавляем автора (пользователь)
    authors_node = sc_utils.createNodeElement(session, segment, sc.SC_CONST)
    sc_utils.createPairPosPerm(session, segment, authors_node, 
                               sc_core.Kernel.getSingleton().getUserAddr(), sc.SC_CONST)
    authors_pair_sheaf = sc_utils.createPairBinaryOrient(session, segment, 
                               q_node, authors_node, sc.SC_CONST)
    sc_utils.createPairPosPerm(session, segment, sc_key.common.nrel_authors, 
                               authors_pair_sheaf, sc.SC_CONST)
    # добавляем окна для вывода
    output_node = sc_utils.createNodeElement(session, segment, sc.SC_CONST)
    sc_utils.copySet(session, sc_key.ui.set_output_windows, output_node, segment)
    # link output windows set to question
    output_sheaf = sc_utils.createPairBinaryOrient(session, segment, output_node, 
                                q_node, sc.SC_CONST)
    sc_utils.createPairPosPerm(session, segment, sc_key.ui.nrel_set_of_output_windows, 
                                output_sheaf, sc.SC_CONST) 
    # initiate question
    sc_utils.createPairPosPerm(session, segment, sc_key.questions.initiated, 
                               q_node, sc.SC_CONST)
    return q_node
    
def out_to_user(sc_set):
    windows = session.search3_f_a_a(sc_key.ui.set_output_windows, sc.SC_A_CONST|sc.SC_POS, sc.SC_N_CONST)
    if windows:
        for els in windows:
            sc_core.Kernel.getSingleton().translateFromSc(sc_set, els[2])
import codecs      
def out_string_to_user(text):
    res = session.create_el(segment, sc.SC_N_CONST)
    set = session.create_el(segment, sc.SC_N_CONST)
#    f = codecs.open("D:/test",'w',encoding="utf-8")
#    f.write(text)
#    f.close()
#    str = unicode(text).decode('iconv:utf-8').encode('iconv:cp1251')
    print text
    sc_utils.setContentStr(session, segment, res, str(text))
    session.gen3_f_a_f(segment, set, res, sc.SC_A_CONST|sc.SC_POS)
    out_to_user(set)