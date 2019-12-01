import logging
import enum

from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData, Enum, JSON, create_engine

logger = logging.getLogger(__name__)

Base = declarative_base()


class DBHelper:
    _engine = None

    @classmethod
    def connect_database(cls, config):
        if cls._engine is None:
            cls._engine = create_engine(config.DATABASE_URI)
            Base.metadata.create_all(cls._engine)

    @classmethod
    def get_session(cls):
        if cls._engine is None:
            raise Exception("Database is not connected")

        return Session(cls._engine)


class DetailStatusEnum(enum.Enum):
    pending = 'pending'
    waiting = 'waiting'
    completed = 'completed'
    failed = 'failed'


class VNCSpecies(Base):
    __tablename__ = 'vnc_species'

    id = Column('id', String(36), primary_key=True, nullable=False)
    name = Column('name', String(100), nullable=False)
    species = Column('species', String(100), nullable=True)
    classname = Column('class', String(100), nullable=True)
    familyname = Column('family', String(100), nullable=True)
    ordername = Column('order', String(100), nullable=True)
    url = Column('url', String(1000), nullable=True)
    detail_status = Column('detail_status', Enum(DetailStatusEnum), default=DetailStatusEnum.pending.value, nullable=False)

    @classmethod
    def create(cls, session, **kwargs):
        obj = cls(**kwargs)
        logger.info("Add entry: %s", kwargs)

        try:
            session.add(obj)
            session.commit()
            return obj
        except (Exception,) as ex:
            session.rollback()
            logger.warning("Create data for table {} error".format(cls.__tablename__))
            logger.warning("Error {}".format(ex))
            return None

    @classmethod
    def get_item(cls, session, **kwargs):
        query = session.query(cls)

        if 'id' in kwargs and kwargs.get('id') is not None:
            query = query.filter(cls.id == kwargs.get('id'))

        if 'detail_status' in kwargs and kwargs.get('detail_status') is not None:
            query = query.filter(cls.detail_status == kwargs.get('detail_status'))

        if 'limit' in kwargs and kwargs.get('limit') is not None:
            query = query.limit(kwargs.get('limit'))

        return query.all()


class VNCSpeciesDetails(Base):
    __tablename__ = 'vnc_species_detail'

    id = Column('id', String(36), primary_key=True, nullable=False)
    details = Column('details', String(10000), nullable=False)

    @classmethod
    def create(cls, session, **kwargs):
        obj = cls(**kwargs)
        logger.info("Add entry: %s", kwargs)

        try:
            session.add(obj)
            session.commit()
            return obj
        except (Exception,) as ex:
            session.rollback()
            logger.warning("Create data for table {} error".format(cls.__tablename__))
            logger.warning("Error {}".format(ex))
            return None


class VNCSpeciesImage(Base):
    __tablename__ = 'vnc_species_image'

    uuid = Column('uuid', String(36), primary_key=True, nullable=False)
    vnc_id = Column('vnc_id', String(36), nullable=False)
    url = Column('url', String(1000), nullable=True)
    vnc_url = Column('vnc_url', String(1000), nullable=False)
    is_valid = Column('is_valid', Integer, default=0)

    @classmethod
    def create(cls, session, **kwargs):
        obj = cls(**kwargs)
        logger.info("Add entry: %s", kwargs)

        try:
            session.add(obj)
            session.commit()
            return obj
        except (Exception,) as ex:
            session.rollback()
            logger.warning("Create data for table {} error".format(cls.__tablename__))
            logger.warning("Error {}".format(ex))
            return None


class ModelLabel(Base):
    __tablename__ = 'model_label'

    id = Column('id', Integer, primary_key=True, nullable=True, autoincrement=True)
    label_id = Column('label_id', Integer, nullable=False)
    model_name = Column('model_name', String(100), nullable=False)
    vnc_id = Column('vnc_id', String(36), nullable=False)

    @classmethod
    def create(cls, session, **kwargs):
        obj = cls(**kwargs)
        logger.info("Add entry: %s", kwargs)

        try:
            session.add(obj)
            session.commit()
            return obj
        except (Exception,) as ex:
            session.rollback()
            logger.warning("Create data for table {} error".format(cls.__tablename__))
            logger.warning("Error {}".format(ex))
            return None
