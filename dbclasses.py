#!/usr/bin/python
# -*- encoding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.orm.collections import attribute_mapped_collection

# If this is True, use separate tables in the database, otherwise use single 
# large table
USE_SEPARATE_TABLES = True
#Verbose output
VERBOSE = True




Base = declarative_base()


class Component(Base):
    '''
    Base class representing a single component
    '''
    #The database table name where this goes
    __tablename__ = 'components'
    #The key
    id = Column(Integer, primary_key=True)
    #A string needed to define sub-classes, the component type
    component_type = Column(String(32), nullable=False)
    #The component name
    name = Column(String(64), nullable=False)
    #This links to a file actually containing our data
    associated_datafile = Column(Text, nullable=True)
    #This is the trick for sub-classing, it tells based on which field
    #you define sub-classes
    __mapper_args__ = { 'polymorphic_on': component_type }
    # Allow for groups of components
    # This is the part that I do not understand well, I copied online :-)
    # Basically: I am creating a one-to-multi relationship, allowing
    # A component to own sub-components. 
    # The backref here after should be a way to keep the navigation
    # in both ways. 
    # Issue: I think in this desing I cannot have a component belonging to
    # two separate groups
    # This is because the relationship parent->daughter is expressed in the 
    # daughter adding a parent. To understand what has to be changed here
    # to allow to specify daughters and forget about parent.
    # see function in testing module called *add_groups*
    # The collecion_class stuff tells to use a dictionary to keep childrens
    # using the property 'name' as key.
    # See: http://docs.sqlalchemy.org/en/latest/_modules/examples/adjacency_list/adjacency_list.html
    parent_id = Column(Integer, ForeignKey(id))
    children = relationship(
        "Component",
        backref=backref("parent",remote_side=id),
        collection_class=attribute_mapped_collection('name')
    )

class Group(Component):
    '''
    A group of components
    This class is needed to allow for a generic component
    '''
    TYPE = 'group'
    __mapper_args__ = { 'polymorphic_identity' : TYPE}

class Quadrupole(Component):
    '''
    A type of componet: Quadrupole
    '''
    TYPE='quadrupole'
    # If the following two lines are present, the quadrupoles are 
    # stored in a separate table, otherwise they are stored in the 
    # same table as the base component, note that in this latter case 
    # the base class table will contain all the properties
    if USE_SEPARATE_TABLES:
        __tablename__ = 'quadrupoles'
        id = Column(None, ForeignKey('components.id'), primary_key=True)
    __mapper_args__ = { 'polymorphic_identity' : TYPE}
    prop1 = Column(Float)

class Crystal(Component):
    '''
    A type of componemt: Crystals
    '''
    TYPE = 'crystal'
    if USE_SEPARATE_TABLES:
        __tablename__ = 'crystals'
        id = Column(None, ForeignKey('components.id'), primary_key=True)
    __mapper_args__ = { 'polymorphic_identity' : TYPE }
    prop2 = Column(Float)

def initialize(verbose=True):
    '''
    Initialize dabase
    :return: engine, session objects
    '''
    eng = create_engine('sqlite:///:memory:', echo=verbose)
    Base.metadata.bind = eng
    Base.metadata.create_all()
    Session = sessionmaker(bind=eng)
    ses = Session()
    return (eng, ses)


# Testing routines
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
    eng, ses = initialize(VERBOSE)
    TestSchema.SESSION = ses
    unittest.main()
    ses.close_all()