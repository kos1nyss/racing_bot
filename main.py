from data.constants import *
from data.db_session import *
from data.all_models import *
from data.functions import *
from random import randint
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import pymorphy2


def send_message(u, t):
    p = {'user_id': u.id,
         'random_id': randint(0, 2 ** 64),
         'message': t,
         'keyboard': get_keyboard(u.status)}
    vk.messages.send(**p)


USERS_QUEUE = []

global_init('race_db')
db_sess = create_session()

statuses = db_sess.query(Status).all()
if not statuses:
    add_statuses()

morph = pymorphy2.MorphAnalyzer()

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, -VK_ID)

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        vk_id = event.obj.message['from_id']
        text = event.obj.message['text']
        message = '-'
        user = db_sess.query(User).filter(User.id == vk_id).first()
        if not user:
            car = Car(max_speed=1, acceleration=1)
            user = User(id=vk_id, status=-1, car=car.id, rating=300)
            db_sess.add(user)

        if user.status == -1:
            user.status = 0
            send_message(user, '🏎️')
        elif user.status == 0:
            if text == 'Гонка':
                user.status = 1
                send_message(user, 'Нажмите "Начать", чтоб запустить поиск гонки')
            elif text == 'Моя машина':
                pass
            elif text == 'Рейтинг':
                rating = user.rating
                p_word = morph.parse('очко')[0].make_agree_with_number(rating).word
                message = f'На данный момент у вас {rating} {p_word}\n\nЛидеры по очкам:\n'
                leaders = db_sess.query(User).order_by(User.rating.desc()).all()
                n = 10
                while n and leaders:
                    ld = leaders.pop(0)
                    u = vk.users.get(user_ids=[ld.id])[0]
                    fullname = f'{u["first_name"]} {u["last_name"]}'
                    message += f'{fullname} - {ld.rating}\n'
                    n -= 1
                send_message(user, message)
            elif text == 'Правила':
                pass
        elif user.status == 1:
            if text == 'Назад':
                user.status = 0
                send_message(user, '🏎️')
            elif text == 'Начать':
                user.status = 2
                send_message(user, 'Ищем подходящего соперника')
                if USERS_QUEUE:
                    rival = USERS_QUEUE.pop(0)
                    racers = [user, rival]
                    for r in racers:
                        r.status = 3
                        send_message(r, 'Найден соперник')
                else:
                    USERS_QUEUE.append(user)
        elif user.status == 2:
            if text == 'Отмена':
                user.status = 1
                send_message(user, 'Поиск гонки отменен')
        elif user.status == 3:
            pass
        db_sess.commit()
