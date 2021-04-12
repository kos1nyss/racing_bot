import json

cancel_keyboard = {"one_time": True,
                   "buttons": [
                       [
                           {
                               'action': {
                                   'type': 'text',
                                   'label': 'Отмена'}
                           },
                       ],
                   ], }
cancel_keyboard = json.dumps(cancel_keyboard)

clear_keyboard = {"one_time": True,
                  "buttons": [
                  ], }
clear_keyboard = json.dumps(clear_keyboard)

main_keyboard = {"one_time": True,
                 "buttons": [
                     [
                         {
                             'action': {
                                 'type': 'text',
                                 'label': 'Гонка'}
                         },
                         {
                             'action': {
                                 'type': 'text',
                                 'label': 'Моя машина'}
                         },
                     ],
                     [
                         {
                             'action': {
                                 'type': 'text',
                                 'label': 'Рейтинг'}
                         },
                         {
                             'action': {
                                 'type': 'text',
                                 'label': 'Правила'}
                         },
                     ],
                 ], }
main_keyboard = json.dumps(main_keyboard)

race_keyboard = {"one_time": True,
                 "buttons": [
                     [
                         {
                             'action': {
                                 'type': 'text',
                                 'label': 'Начать'}
                         },
                         {
                             'action': {
                                 'type': 'text',
                                 'label': 'Назад'}
                         },
                     ],
                 ], }
race_keyboard = json.dumps(race_keyboard)

keyboards = {0: main_keyboard,
             1: race_keyboard,
             2: cancel_keyboard,
             3: clear_keyboard}
