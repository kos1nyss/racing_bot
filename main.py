from data.constants import *
from data.db_session import *
from data.all_models import *
from data.functions import *
from data.race import *
from random import randint
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import pymorphy2


def send_message(u, t, attachment=None):
    p = {'user_id': u.id,
         'random_id': randint(0, 2 ** 64),
         'message': t,
         'keyboard': get_keyboard(u.status)}
    if attachment:
        p['attachment'] = attachment
    vk.messages.send(**p)


def get_fullname(u):
    u = vk.users.get(user_ids=[u.id])[0]
    return f'{u["first_name"]} {u["last_name"]}'


S = 1000
USERS_QUEUE = []

global_init('race_db')
db_sess = create_session()

statuses = db_sess.query(Status).all()
if not statuses:
    add_statuses()

morph = pymorphy2.MorphAnalyzer()

vk_session = vk_api.VkApi(login=LOGIN, password=PASSWORD, token=TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, -VK_ID)
upload = vk_api.VkUpload(vk)

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        vk_id = event.obj.message['from_id']
        text = event.obj.message['text']
        message = '-'
        user = db_sess.query(User).filter(User.id == vk_id).first()
        if not user:
            ids = db_sess.query(Car).all()
            if ids:
                max_id = max(ids, key=lambda c: c.id).id
            else:
                max_id = 0
            car = Car(id=max_id + 1, max_speed=1, acceleration=1)
            db_sess.add(car)
            user = User(id=vk_id, status=-1, car_id=car.id, rating=1000)
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
                n = 1
                while n <= 10 and leaders:
                    ld = leaders.pop(0)
                    message += f'{n}. [id{ld.id}|{get_fullname(ld)}] - {ld.rating}\n'
                    n += 1
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
                        for rv in racers:
                            if rv != r:
                                message = f'Найден соперник. Твоим соперником будет [id{rv.id}|{get_fullname(rv)}]'
                                break
                        send_message(r, message)
                    user_car = db_sess.query(Car).filter(Car.id == user.car_id).first()
                    rival_car = db_sess.query(Car).filter(Car.id == rival.car_id).first()
                    race = Race(user_car, rival_car)
                    race.execute(S)
                    gifs = race.get_content()
                    car_winner = race.get_winner()
                    winner = db_sess.query(User).filter(User.car_id == car_winner.id).first()
                    for i in range(2):
                        racers[i].status = 0
                        gif = upload.document_message(gifs[i], peer_id=racers[i].id, )
                        doc = gif['doc']
                        owner_id, doc_id = doc['owner_id'], doc['id']
                        if racers[i] == winner:
                            message = 'Поздравляю!!! Ты победил!'
                        else:
                            message = 'Повезет в следующий раз'
                        send_message(racers[i], message, attachment=f'doc{owner_id}_{doc_id}')

                else:
                    USERS_QUEUE.append(user)
        elif user.status == 2:
            if text == 'Отмена':
                user.status = 1
                send_message(user, 'Поиск гонки отменен')
        elif user.status == 3:
            pass
        db_sess.commit()
