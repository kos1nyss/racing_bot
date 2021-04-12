from .db_session import create_session
from .all_models import Status
from .keyboards import keyboards


def add_statuses():
    db_sess = create_session()
    db_sess.add(Status(id=-1, title='Not started'))
    db_sess.add(Status(id=0, title='In then main menu'))
    db_sess.add(Status(id=1, title='Starting a race'))
    db_sess.add(Status(id=2, title='Waiting a race'))
    db_sess.add(Status(id=3, title='In the race'))
    db_sess.commit()
    db_sess.close()


def get_keyboard(status):
    return keyboards[status]