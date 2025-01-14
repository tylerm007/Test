# created from response - used to create database and project
#  should run without error
#  if not, check for decimal, indent, or import issues

import decimal

import logging



logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

import sqlalchemy



from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py

from logic_bank.logic_bank import Rule

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

# Define the database path
DATABASE_URL = "sqlite:///system/genai/temp/create_db_models.sqlite"

# Define the data model classes

class Farm(Base):
    """description: A farm entity which manages multiple barns and workers."""
    __tablename__ = 'farms'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=True)

class Barn(Base):
    """description: A barn where multiple pens are located within a farm."""
    __tablename__ = 'barns'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    farm_id = Column(Integer, ForeignKey('farms.id'), nullable=False)

class Pen(Base):
    """description: A pen used to house cattle within a barn."""
    __tablename__ = 'pens'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    barn_id = Column(Integer, ForeignKey('barns.id'), nullable=False)

class Cattle(Base):
    """description: Represents individual cattle with their specific details."""
    __tablename__ = 'cattles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag_number = Column(String, nullable=False, unique=True)
    birth_date = Column(DateTime, nullable=True)

class CattlePen(Base):
    """description: Junction table to assign cattle to pens."""
    __tablename__ = 'cattle_pens'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cattle_id = Column(Integer, ForeignKey('cattles.id'), nullable=False)
    pen_id = Column(Integer, ForeignKey('pens.id'), nullable=False)
    assignment_date = Column(DateTime, nullable=True, default=datetime.datetime.now)

class Employee(Base):
    """description: Employees who work on a farm and manage barns and pens."""
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=True)
    farm_id = Column(Integer, ForeignKey('farms.id'), nullable=False)

class FeedingSchedule(Base):
    """description: Feeding schedule detailing what and when cattle are fed."""
    __tablename__ = 'feeding_schedules'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pen_id = Column(Integer, ForeignKey('pens.id'), nullable=False)
    feed_type = Column(String, nullable=False)
    schedule_time = Column(DateTime, nullable=False)

class HealthCheck(Base):
    """description: Captures health check records for each cattle."""
    __tablename__ = 'health_checks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cattle_id = Column(Integer, ForeignKey('cattles.id'), nullable=False)
    check_date = Column(DateTime, nullable=True)
    health_status = Column(String, nullable=True)
    notes = Column(String, nullable=True)

class Supplier(Base):
    """description: Suppliers providing resources and goods for the farm."""
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    contact_info = Column(String, nullable=True)

class SupplyOrder(Base):
    """description: Orders placed with suppliers for farm needs."""
    __tablename__ = 'supply_orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=False)
    order_date = Column(DateTime, nullable=True)
    delivery_date = Column(DateTime, nullable=True)

class SupplyItem(Base):
    """description: Details of items supplied in each order."""
    __tablename__ = 'supply_items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('supply_orders.id'), nullable=False)
    item_name = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)

class Veterinary(Base):
    """description: Veterinarians associated with the farm for cattle care."""
    __tablename__ = 'veterinaries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    contact_number = Column(String, nullable=True)

class VetVisit(Base):
    """description: Veterinary visits and services provided to farm cattle."""
    __tablename__ = 'vet_visits'
    id = Column(Integer, primary_key=True, autoincrement=True)
    veterinary_id = Column(Integer, ForeignKey('veterinaries.id'), nullable=False)
    cattle_id = Column(Integer, ForeignKey('cattles.id'), nullable=False)
    visit_date = Column(DateTime, nullable=True)
    treatment = Column(String, nullable=True)

# Setup the database
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Add sample data
farm = Farm(name='Green Pastures Farm', location='450 Farm Ln, Sunnyvale')
barn1 = Barn(name='North Barn', farm_id=1)
barn2 = Barn(name='South Barn', farm_id=1)
pen1 = Pen(name='Pen A', barn_id=1)
pen2 = Pen(name='Pen B', barn_id=1)
cattle1 = Cattle(tag_number='C123', birth_date=datetime.datetime(2020, 6, 1))
cattle2 = Cattle(tag_number='C124', birth_date=datetime.datetime(2021, 8, 15))
cattle_pen1 = CattlePen(cattle_id=1, pen_id=1, assignment_date=datetime.datetime.now())
cattle_pen2 = CattlePen(cattle_id=2, pen_id=2, assignment_date=datetime.datetime.now())
emp1 = Employee(name='John Doe', role='Farm Manager', farm_id=1)
emp2 = Employee(name='Jane Smith', role='Barn Supervisor', farm_id=1)
feeding_schedule1 = FeedingSchedule(pen_id=1, feed_type='Grass', schedule_time=datetime.datetime(2023, 10, 14, 8, 0))
feeding_schedule2 = FeedingSchedule(pen_id=2, feed_type='Corn', schedule_time=datetime.datetime(2023, 10, 14, 18, 0))
health_check1 = HealthCheck(cattle_id=1, check_date=datetime.datetime.now(), health_status='Healthy', notes='Routine Check')
health_check2 = HealthCheck(cattle_id=2, check_date=datetime.datetime.now(), health_status='Needs Vaccination', notes='')
supplier = Supplier(name='Agri Supply Co.', contact_info='agri@supplies.com')
supply_order = SupplyOrder(supplier_id=1, order_date=datetime.datetime.now(), delivery_date=datetime.datetime(2023, 11, 5))
supply_item1 = SupplyItem(order_id=1, item_name='Barley', quantity=500)
supply_item2 = SupplyItem(order_id=1, item_name='Hay', quantity=1000)
vet = Veterinary(name='Dr. Emily Clark', contact_number='555-1234')
vet_visit = VetVisit(veterinary_id=1, cattle_id=1, visit_date=datetime.datetime.now(), treatment='Deworming')

# Add instances to session
session.add_all([farm, barn1, barn2, pen1, pen2, cattle1, cattle2, cattle_pen1, cattle_pen2, 
                 emp1, emp2, feeding_schedule1, feeding_schedule2, health_check1, health_check2,
                 supplier, supply_order, supply_item1, supply_item2, vet, vet_visit])

# Commit the session
session.commit()

# Close the session
session.close()
