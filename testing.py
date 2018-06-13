#!/usr/bin/python
# -*- encoding: utf-8 -*-

from dbclasses import Base, Quadrupole, Crystal, Component, Group
from dbclasses import USE_SEPARATE_TABLES, initialize, VERBOSE
from sqlalchemy.orm import sessionmaker
import unittest

class TestSchema(unittest.TestCase):
    SESSION = None
    def test1_add_quads(self):
        ''' 
        Test adding two quadrupoles
        ''' 
        q1 = Quadrupole(name='Q1', component_type=Quadrupole.TYPE, prop1=1.2)
        q2 = Quadrupole(name='Q2', component_type=Quadrupole.TYPE, prop1=2.2)
        self.SESSION.add_all([q1, q2])
        self.SESSION.commit()

    def test1_add_group(self):
        '''
        Test adding group of quadrupoles
        '''
        q1 = Quadrupole(name='Q3', component_type=Quadrupole.TYPE, prop1=3.1)
        q2 = Quadrupole(name='Q4', component_type=Quadrupole.TYPE, prop1=4.1)
        g1 = Group(name='G1', component_type=Group.TYPE)
        q1.parent = g1
        q2.parent = g1
        self.assertEquals(g1.children['Q3'].prop1,3.1)

        q3 = Quadrupole(name='Q5', component_type=Quadrupole.TYPE, prop1=5.1)
        g2 = Group(name='G2', component_type=Group.TYPE)
        q3.parent = g2
        g1.parent = g2
        self.SESSION.add_all([q1,q2,g1,q3,g2])
        #g = Group(name='G1', component_type=Group.TYPE)
        #g.children.append(q1)
        #self.SESSION.add_all([q1,q2,g])
        #self.SESSION.commit()

    def test1_add_crystals(self):
        '''
        Test adding two crystals
        '''
        c1 = Crystal(name='C1', component_type=Crystal.TYPE, prop2=0.1)
        c2 = Crystal(name='C2', component_type=Crystal.TYPE, prop2=0.2)
        self.SESSION.add_all([c1,c2])
        self.SESSION.commit()

    def test2_read_quads(self):
        '''
        Test reading back quadrupoles
        '''
        result = self.SESSION.query(Quadrupole).all()
        self.assertEqual(len(result),5)
        print('Quadrupoles:')
        for q in result:
            print(q.id,q.name,q.component_type,q.prop1)
            self.assertGreater(q.prop1,1)

    def test2_read_crystals(self):
        '''
        Test reading back crystals
        '''
        result = self.SESSION.query(Crystal).all()
        self.assertEqual(len(result),2)
        print('Crystals:')
        for q in result:
            print(q.id,q.name,q.component_type,q.prop2)
            self.assertLess(q.prop2,1)

    def test2_read_groups(self):
        '''
        Test reading groups of components back
        '''
        #Query all objects in the components database
        #verify that the two we called 'G1' and 'G2' have
        #indeed children
        result = self.SESSION.query(Component).all()
        for r in result:
            print("This component (%s) has: %d  sub-components"%(r.name,len(r.children)))
            if r.name == 'G1' or r.name == 'G2':
                self.assertGreater(len(r.children),0)
        result = self.SESSION.query(Group).all()
        for r in result:
            self.assertGreater(len(r.children),0)
        # Now show navigation, in the DB there is a tree:
        # G2 --+-- Q5
        #      +-- G1 --+-- Q3
        #               +-- Q4
        result = self.SESSION.query(Component).\
                filter(Component.name=='G2').all()
        self.assertEqual(len(result),1)
        r=result[0]
        self.assertEqual(len(r.children),2)
        gr = r.children['G1']
        self.assertTrue(isinstance(gr,Group))
        self.assertEqual(len(gr.children),2)
        quad = r.children['Q5']
        self.assertEqual(len(quad.children),0)
        self.assertTrue(isinstance(quad,Quadrupole))

if __name__ == '__main__':
    print("Using separate tables:",USE_SEPARATE_TABLES)
    eng, ses = initialize(VERBOSE)
    TestSchema.SESSION = ses
    unittest.main()
    ses.close_all()