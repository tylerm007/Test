# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  October 30, 2024 17:15:38
# Database: sqlite:////tmp/tmp.cLYs4vJl6H/Test/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Cattle(SAFRSBaseX, Base):
    """
    description: Represents individual cattle with their specific details.
    """
    __tablename__ = 'cattles'
    _s_collection_name = 'Cattle'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    tag_number = Column(String, nullable=False, unique=True)
    birth_date = Column(DateTime)

    # parent relationships (access parent)

    # child relationships (access children)
    HealthCheckList : Mapped[List["HealthCheck"]] = relationship(back_populates="cattle")
    VetVisitList : Mapped[List["VetVisit"]] = relationship(back_populates="cattle")
    CattlePenList : Mapped[List["CattlePen"]] = relationship(back_populates="cattle")



class Farm(SAFRSBaseX, Base):
    """
    description: A farm entity which manages multiple barns and workers.
    """
    __tablename__ = 'farms'
    _s_collection_name = 'Farm'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    BarnList : Mapped[List["Barn"]] = relationship(back_populates="farm")
    EmployeeList : Mapped[List["Employee"]] = relationship(back_populates="farm")



class Supplier(SAFRSBaseX, Base):
    """
    description: Suppliers providing resources and goods for the farm.
    """
    __tablename__ = 'suppliers'
    _s_collection_name = 'Supplier'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_info = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    SupplyOrderList : Mapped[List["SupplyOrder"]] = relationship(back_populates="supplier")



class Veterinary(SAFRSBaseX, Base):
    """
    description: Veterinarians associated with the farm for cattle care.
    """
    __tablename__ = 'veterinaries'
    _s_collection_name = 'Veterinary'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_number = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    VetVisitList : Mapped[List["VetVisit"]] = relationship(back_populates="veterinary")



class Barn(SAFRSBaseX, Base):
    """
    description: A barn where multiple pens are located within a farm.
    """
    __tablename__ = 'barns'
    _s_collection_name = 'Barn'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    farm_id = Column(ForeignKey('farms.id'), nullable=False)

    # parent relationships (access parent)
    farm : Mapped["Farm"] = relationship(back_populates=("BarnList"))

    # child relationships (access children)
    PenList : Mapped[List["Pen"]] = relationship(back_populates="barn")



class Employee(SAFRSBaseX, Base):
    """
    description: Employees who work on a farm and manage barns and pens.
    """
    __tablename__ = 'employees'
    _s_collection_name = 'Employee'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(String)
    farm_id = Column(ForeignKey('farms.id'), nullable=False)

    # parent relationships (access parent)
    farm : Mapped["Farm"] = relationship(back_populates=("EmployeeList"))

    # child relationships (access children)



class HealthCheck(SAFRSBaseX, Base):
    """
    description: Captures health check records for each cattle.
    """
    __tablename__ = 'health_checks'
    _s_collection_name = 'HealthCheck'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    cattle_id = Column(ForeignKey('cattles.id'), nullable=False)
    check_date = Column(DateTime)
    health_status = Column(String)
    notes = Column(String)

    # parent relationships (access parent)
    cattle : Mapped["Cattle"] = relationship(back_populates=("HealthCheckList"))

    # child relationships (access children)



class SupplyOrder(SAFRSBaseX, Base):
    """
    description: Orders placed with suppliers for farm needs.
    """
    __tablename__ = 'supply_orders'
    _s_collection_name = 'SupplyOrder'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    supplier_id = Column(ForeignKey('suppliers.id'), nullable=False)
    order_date = Column(DateTime)
    delivery_date = Column(DateTime)

    # parent relationships (access parent)
    supplier : Mapped["Supplier"] = relationship(back_populates=("SupplyOrderList"))

    # child relationships (access children)
    SupplyItemList : Mapped[List["SupplyItem"]] = relationship(back_populates="order")



class VetVisit(SAFRSBaseX, Base):
    """
    description: Veterinary visits and services provided to farm cattle.
    """
    __tablename__ = 'vet_visits'
    _s_collection_name = 'VetVisit'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    veterinary_id = Column(ForeignKey('veterinaries.id'), nullable=False)
    cattle_id = Column(ForeignKey('cattles.id'), nullable=False)
    visit_date = Column(DateTime)
    treatment = Column(String)

    # parent relationships (access parent)
    cattle : Mapped["Cattle"] = relationship(back_populates=("VetVisitList"))
    veterinary : Mapped["Veterinary"] = relationship(back_populates=("VetVisitList"))

    # child relationships (access children)



class Pen(SAFRSBaseX, Base):
    """
    description: A pen used to house cattle within a barn.
    """
    __tablename__ = 'pens'
    _s_collection_name = 'Pen'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    barn_id = Column(ForeignKey('barns.id'), nullable=False)

    # parent relationships (access parent)
    barn : Mapped["Barn"] = relationship(back_populates=("PenList"))

    # child relationships (access children)
    CattlePenList : Mapped[List["CattlePen"]] = relationship(back_populates="pen")
    FeedingScheduleList : Mapped[List["FeedingSchedule"]] = relationship(back_populates="pen")



class SupplyItem(SAFRSBaseX, Base):
    """
    description: Details of items supplied in each order.
    """
    __tablename__ = 'supply_items'
    _s_collection_name = 'SupplyItem'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('supply_orders.id'), nullable=False)
    item_name = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)

    # parent relationships (access parent)
    order : Mapped["SupplyOrder"] = relationship(back_populates=("SupplyItemList"))

    # child relationships (access children)



class CattlePen(SAFRSBaseX, Base):
    """
    description: Junction table to assign cattle to pens.
    """
    __tablename__ = 'cattle_pens'
    _s_collection_name = 'CattlePen'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    cattle_id = Column(ForeignKey('cattles.id'), nullable=False)
    pen_id = Column(ForeignKey('pens.id'), nullable=False)
    assignment_date = Column(DateTime)

    # parent relationships (access parent)
    cattle : Mapped["Cattle"] = relationship(back_populates=("CattlePenList"))
    pen : Mapped["Pen"] = relationship(back_populates=("CattlePenList"))

    # child relationships (access children)



class FeedingSchedule(SAFRSBaseX, Base):
    """
    description: Feeding schedule detailing what and when cattle are fed.
    """
    __tablename__ = 'feeding_schedules'
    _s_collection_name = 'FeedingSchedule'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    pen_id = Column(ForeignKey('pens.id'), nullable=False)
    feed_type = Column(String, nullable=False)
    schedule_time = Column(DateTime, nullable=False)

    # parent relationships (access parent)
    pen : Mapped["Pen"] = relationship(back_populates=("FeedingScheduleList"))

    # child relationships (access children)
