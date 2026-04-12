from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    systems = relationship("System", back_populates="project")

class System(Base):
    __tablename__ = "systems"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="systems")
    subassemblies = relationship("Subassembly", back_populates="system")

class Subassembly(Base):
    __tablename__ = "subassemblies"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    system_id = Column(Integer, ForeignKey("systems.id"))
    system = relationship("System", back_populates="subassemblies")
    cards = relationship("Card", back_populates="subassembly")

class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    subassembly_id = Column(Integer, ForeignKey("subassemblies.id"))
    subassembly = relationship("Subassembly", back_populates="cards")

class Fault(Base):
    __tablename__ = "faults"
    id = Column(Integer, primary_key=True)
    level = Column(String, nullable=False)
    level_id = Column(Integer, nullable=False)
    description = Column(String, nullable=False)