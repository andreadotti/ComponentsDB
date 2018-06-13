#!/usr/bin/python
# -*- encoding: utf-8 -*-

from dbclasses import Base, Quadrupole, Crystal, Component
from dbclasses import USE_SEPARATE_TABLES, initialize
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
        self.assertEqual(len(result),2)
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


if __name__ == '__main__':
    print("Using separate tables:",USE_SEPARATE_TABLES)
    eng, ses = initialize()
    TestSchema.SESSION = ses
    unittest.main()
    ses.close_all()