from .db_session import create_session
from .all_models import Status
from .keyboards import keyboards


def add_statuses() -> None:
    db_sess = create_session()
    db_sess.add(Status(id=-1, title='Не начал'))
    db_sess.add(Status(id=0, title='В главном меню'))
    db_sess.add(Status(id=1, title='Начинает гонку'))
    db_sess.add(Status(id=2, title='В поиске соперника для гонки'))
    db_sess.add(Status(id=3, title='В гонке'))
    db_sess.add(Status(id=4, title='Приглашает друзей'))
    db_sess.add(Status(id=5, title='В меню машины'))
    db_sess.add(Status(id=6, title='Прокачивает машину'))
    db_sess.add(Status(id=7, title='В меню профиля'))
    db_sess.add(Status(id=8, title='В общем чате'))
    db_sess.commit()
    db_sess.close()


def get_keyboard(status: int) -> str:
    return keyboards[status]
