import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

SqlAlchemyBase = declarative_base()

__factory = None


def global_init(db_name):
    global __factory

    if __factory:
        return

    conn_str = f'postgresql://postgres:Kostya@localhost:5432/{db_name}'
    engine = sqlalchemy.create_engine(conn_str, echo=False)
    __factory = sqlalchemy.orm.sessionmaker(bind=engine)

    from . import all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session():
    global __factory
    return __factory()
