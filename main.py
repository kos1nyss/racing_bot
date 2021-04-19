from data.constants import *
from data.db_session import *
from data.all_models import *
from data.functions import *
from data.race import *
from random import randint
import datetime as dt
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import pymorphy2


def send_message(u: User, t: str, attachment=None) -> None:
    p = {'user_id': u.id,
         'random_id': randint(0, 2 ** 64),
         'message': t,
         'keyboard': get_keyboard(u.status)}
    if attachment:
        p['attachment'] = attachment
    vk.messages.send(**p)


def error_message(u: User) -> None:
    send_message(u, 'Данная команда сейчас недоступна')


def get_fullname(u: User) -> str:
    u = vk.users.get(user_ids=[u.id])[0]
    return f'{u["first_name"]} {u["last_name"]}'


MAX_CH = 50
S = 1000
USERS_QUEUE = []
PUBLIC_CHAT = []

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
        start_points = randint(8, 12)
        if not user:
            ids = db_sess.query(Car).all()
            if ids:
                max_id = max(ids, key=lambda c: c.id).id
            else:
                max_id = 0
            car = Car(id=max_id + 1, max_speed=1, acceleration=1, turbo=0)
            db_sess.add(car)
            user = User(id=vk_id, status=-1, car_id=car.id, rating=1000, upgrade_points=start_points)
            db_sess.add(user)

        if user.status == -1:
            user.status = 0
            invite = db_sess.query(InvitedUsers).filter(InvitedUsers.id == user.id).first()
            send_message(user, 'Добро пожаловать игру! Желаем удачи в твоих будущих заездах 😄')
            if invite:
                invite.in_game = True
                points = randint(3, 5)
                owner = db_sess.query(User).filter(User.id == invite.owner_id).first()
                owner_fullname = get_fullname(owner)
                user_fullname = get_fullname(user)
                p_word = morph.parse('очко')[0].make_agree_with_number(points).word
                send_message(user, f'Вы зашли по приглашению гонщика [id{user.id}|{owner_fullname}].'
                                   f' Он получит {points} {p_word} прокачки за это')
                send_message(owner,
                             f'[id{user.id}|{get_fullname(owner)}] зашел в игру по вашему '
                             f'приглашению. Поздравляем вы получили {points} {p_word} '
                             f'прокачки!')
                owner.upgrade_points += points
            c_word = morph.parse('очко')[0].make_agree_with_number(start_points).word
            send_message(user, f'Тебе зачислили {start_points} {c_word} прокачки для улучшения '
                               f'твоей машины')
        elif user.status == 0:
            if text == 'Гонка 🏎️':
                user.status = 1
                send_message(user, 'Нажмите "Начать", чтоб запустить поиск гонки')
            elif text == 'Моя машина 🚗':
                user.status = 5
                send_message(user, 'В гонках всегда решает на сколько у тебя мощная машина, это '
                                   'всегда залог успеха')
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
                send_message(user, 'В гонках всегда побеждает машина, более сильная по характери'
                                   'стикам. Чтоб получить очки прокачки машины, приглашай друзей')
            elif text == 'Пригласить друзей 👋':
                user.status = 4
                send_message(user, 'Отравьте ссылку на профиль человека, которого хотите пригласить.'
                                   ' Вы получите очки прокачки, как только он в первый раз зайдет в '
                                   'игру. Не забудьте упомянуть ему лично, что вы его пригласили.')
            elif text == 'Профиль':
                user.status = 7
                send_message(user, 'Тут ты можешь узнать статистику своей игры и посмотреть '
                                   'результаты своих последних заездов')
            elif text == 'Чат':
                user.status = 8
                send_message(user, 'Вы вошли в общий чат. Теперь все ваши сообщения буду видеть все,'
                                   ' кто также находится в общем чате. Отправить \"Выйти\" или '
                                   'нажмите соответствующую кнопку, чтоб выйти в главное меню')
                PUBLIC_CHAT.append(user)
            else:
                error_message(user)
        elif user.status == 1:
            if text == 'Назад 🔙':
                user.status = 0
                send_message(user, '🏎️')
            elif text == 'Начать':
                user.status = 2
                send_message(user, 'Ищем подходящего соперника')
                correct_rivals = [r for r in USERS_QUEUE if
                                  user.rating - 50 < user.rating < user.rating + 50]
                if correct_rivals:
                    rival = correct_rivals.pop(0)
                    racers = [user, rival]
                    for r in racers:
                        r.status = 3
                        for rv in racers:
                            if rv != r:
                                message = f'Найден соперник. Твоим соперником будет ' \
                                          f'[id{rv.id}|{get_fullname(rv)}] ({rv.rating})'
                                break
                        send_message(r, message)
                    user_car = db_sess.query(Car).filter(Car.id == user.car_id).first()
                    rival_car = db_sess.query(Car).filter(Car.id == rival.car_id).first()
                    race = Race(user_car, rival_car)
                    race.execute(S)
                    gifs = race.get_content()
                    car_winner = race.get_winner()
                    winner = db_sess.query(User).filter(User.car_id == car_winner.id).first()
                    delta_points = randint(4, 8)
                    for i in range(2):
                        racers[i].status = 0
                        gif = upload.document_message(gifs[i], peer_id=racers[i].id, )
                        doc = gif['doc']
                        owner_id, doc_id = doc['owner_id'], doc['id']
                        if racers[i] == winner:
                            racers[i].rating += delta_points
                            message = f'Поздравляю!!! Ты победил! Ты получаешь {delta_points} ' \
                                      f'рейтинга'
                        else:
                            racers[i].rating -= delta_points
                            message = f'Повезет в следующий раз. Ты теряешь {delta_points} рейтинга'
                        send_message(racers[i], message, attachment=f'doc{owner_id}_{doc_id}')
                    db_sess.add(Result(user1=user.id, user2=rival.id,
                                       winner=winner.id, time=dt.datetime.now().timestamp()))
                else:
                    USERS_QUEUE.append(user)
            else:
                error_message(user)
        elif user.status == 2:
            if text == 'Отмена 🔙':
                USERS_QUEUE.remove(user)
                user.status = 1
                send_message(user, 'Поиск гонки отменен')
            else:
                error_message(user)
        elif user.status == 3:
            send_message(user, 'Вы в гонке, никакие другие функции сейчас недоступны')
        elif user.status == 4:
            if text == 'Назад 🔙':
                user.status = 0
                send_message(user, 'Чем больше приглашешь друзей, тем мощнее у тебя машина')
            else:
                nickname = text[15:]
                try:
                    friends = vk.users.get(user_ids=[nickname])
                    if friends:
                        friend = friends[0]
                        if db_sess.query(User).filter(User.id == friend['id']).first():
                            send_message(user,
                                         'Этот пользователь уже играет в игру, его нельзя '
                                         'пригласить. Пригласите кого-то другого или '
                                         'нажмите \"Назад\"')
                        elif db_sess.query(InvitedUsers).filter(
                                InvitedUsers.id == friend['id']).first():
                            send_message(user,
                                         'Кто-то уже пригласил это пользователя в игру, его нельзя '
                                         'пригласить. Пригласите кого-то другого или нажмите '
                                         '\"Назад\"')
                        else:
                            db_sess.add(
                                InvitedUsers(id=friend['id'], owner_id=user.id, in_game=False))
                            send_message(user, f'Вы пригласила пользователя [id{friend["id"]}|'
                                               f'{friend["first_name"]} {friend["last_name"]}] '
                                               f'в игру, не забудьте упомянуть ему об этом лично. '
                                               f'Пригласите кого-то еще или нажмите \"Назад\" '
                                               f'для выхода в главное меню')
                    else:
                        error_message(user)
                except vk_api.exceptions.ApiError:
                    send_message(user, 'Вы отправили некорректную ссылку. Попробуйте ещё раз '
                                       'или нажмите кнопку \"Назад\" для выхода в главное меню')
        elif user.status == 5:
            if text == 'Характеристики':
                car = db_sess.query(Car).filter(Car.id == user.car_id).first()
                send_message(user, f'Твоя машина:\n'
                                   f'· Максимальная скорость - {car.max_speed}/{MAX_CH}\n'
                                   f'· Ускорение - {car.max_speed}/{MAX_CH}\n'
                                   f'· Турбо - {car.turbo}/{MAX_CH} (включается, после того как '
                                   f'гонщик проехал половину трассы)\n')
            elif text == 'Прокачать':
                user.status = 6
                p_word = morph.parse('очко')[0].make_agree_with_number(user.upgrade_points).word
                send_message(user, f'У вас {user.upgrade_points} {p_word}. Используй их чтоб '
                                   f'прокачать свою машину. Выбери что хочешь прокачать')
            elif text == 'Назад 🔙':
                user.status = 0
                send_message(user, 'Возвращайся в свой гараж почаще')
            else:
                error_message(user)
        elif user.status == 6:
            car = db_sess.query(Car).filter(Car.id == user.car_id).first()
            if text == 'Назад 🔙':
                user.status = 5
                send_message(user, 'Теперь давай в гонку! Покажи всем какая у тебя быстрая тачка')
            elif user.upgrade_points == 0:
                user.status = 5
                send_message(user, 'У тебя не хватает очков, чтоб прокачать характеристики машины')
            elif text == 'М. скорость':
                if car.max_speed == MAX_CH:
                    send_message(user, 'Максимальная скорость уже прокачена на максимум')
                else:
                    car.max_speed += 1
                    user.upgrade_points -= 1
                    send_message(user, 'Вы удачно прокачали вашу машину')
            elif text == 'Ускорение':
                if car.acceleration == MAX_CH:
                    send_message(user, 'Ускорение уже прокачено на максимум,'
                                       ' прокачайте что-то другое')
                else:
                    car.acceleration += 1
                    user.upgrade_points -= 1
                    send_message(user, 'Вы улучшили ускорение вашей машины')
            elif text == 'Турбо':
                if car.turbo == MAX_CH:
                    send_message(user, 'Турбо уже прокачено на максимум')
                else:
                    car.turbo += 1
                    user.upgrade_points -= 1
                    send_message(user, 'Теперь в вашей машине стоит более мощное турбо')
            else:
                error_message(user)
        elif user.status == 7:
            if text == 'Обо мне':
                races = db_sess.query(Result).filter(
                    (Result.user1 == user.id) | (Result.user2 == user.id)).all()
                wins = db_sess.query(Result).filter(Result.winner == user.id).all()
                invited = db_sess.query(InvitedUsers).filter(InvitedUsers.owner_id == user.id).all()
                used_invitations = db_sess.query(InvitedUsers).filter(
                    InvitedUsers.owner_id == user.id, InvitedUsers.in_game.is_(True)).all()
                percent = "{:.2f}%".format(len(wins) / len(races) * 100) \
                    if races else "не сыграно ни одной гонки"
                send_message(user, f'[id{user.id}|{get_fullname(user)}] ({user.rating})\n'
                                   f'· Гонок: {len(races)}\n'
                                   f'· Побед: {len(wins)}\n'
                                   f'· Процент побед: {percent}\n'
                                   f'· Пригласил в игру: {len(invited)}\n'
                                   f'· Зашли в игру по приглашению: {len(used_invitations)}')
            elif text == 'Последние заезды':
                message = 'Надеемся ты будешь доволен результатами своих заездов\n\n'
                races = db_sess.query(Result).filter(
                    (Result.user1 == user.id) | (Result.user2 == user.id)).order_by(
                    Result.time).all()
                n = 0
                while n < 10 and races:
                    r = races.pop()
                    result = 'ПОБЕДА' if r.winner == user.id else 'ПОРАЖЕНИЕ'
                    rival_id = r.user1 if r.user2 == user.id else r.user2
                    rival = db_sess.query(User).filter(User.id == rival_id).first()
                    delta_time = dt.datetime.now().timestamp() - r.time
                    if delta_time < 3600:
                        time_text = 'меньше часа назад'
                    elif delta_time < 3600 * 24:
                        time_text = 'сегодня'
                    else:
                        time_text = 'несколько дней назад'
                    message += f'· {result} против [id{rival_id}|{get_fullname(rival)}] - ' \
                               f'{time_text}\n'
                send_message(user, message)

            elif text == 'Назад 🔙':
                user.status = 0
                send_message(user, 'Удачи в гонках! ')
            else:
                error_message(user)
        elif user.status == 8:
            if text == 'Выйти 🔙':
                PUBLIC_CHAT.remove(user)
                user.status = 0
                send_message(user, 'Вы покинули общий чат')
            else:
                for u in PUBLIC_CHAT:
                    if u != user:
                        send_message(u, f'[id{u.id}|{get_fullname(u)}]: {text}')
    db_sess.commit()
