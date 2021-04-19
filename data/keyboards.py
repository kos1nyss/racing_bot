import json

cancel_keyboard = {"one_time": True,
                   "buttons": [
                       [
                           {
                               'action': {
                                   'type': 'text',
                                   'label': 'Отмена 🔙'},
                               'color': 'negative'
                           },
                       ],
                   ], }
cancel_keyboard = json.dumps(cancel_keyboard)

back_keyboard = {"one_time": True,
                 "buttons": [
                     [
                         {
                             'action': {
                                 'type': 'text',
                                 'label': 'Назад 🔙'},
                             'color': 'negative'
                         },
                     ],
                 ], }
back_keyboard = json.dumps(back_keyboard)

exit_keyboard = {"one_time": True,
                 "buttons": [
                     [
                         {
                             'action': {
                                 'type': 'text',
                                 'label': 'Выйти 🔙'},
                             'color': 'negative'
                         },
                     ],
                 ], }
exit_keyboard = json.dumps(exit_keyboard)

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
                                 'label': 'Гонка 🏎️'},
                             'color': 'primary'
                         },
                         {
                             'action': {
                                 'type': 'text',
                                 'label': 'Моя машина 🚗'},
                             'color': 'primary'
                         },
                     ],
                     [
                         {
                             'action': {
                                 'type': 'text',
                                 'label': 'Рейтинг', }
                         },
                         {
                             'action': {
                                 'type': 'text',
                                 'label': 'Правила'}
                         },
                     ],
                     [
                         {
                             'action': {
                                 'type': 'text',
                                 'label': 'Профиль'},
                             'color': 'primary'
                         },
                         {
                             'action': {
                                 'type': 'text',
                                 'label': 'Чат'}
                         },
                     ],
                     [
                         {
                             'action': {
                                 'type': 'text',
                                 'label': 'Пригласить друзей 👋'},
                             'color': 'primary'
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
                                 'label': 'Начать'},
                             'color': 'positive'
                         },
                         {
                             'action': {
                                 'type': 'text',
                                 'label': 'Назад 🔙'},
                             'color': 'negative'
                         },
                     ],
                 ], }
race_keyboard = json.dumps(race_keyboard)

car_keyboard = {"one_time": True,
                "buttons": [
                    [
                        {
                            'action': {
                                'type': 'text',
                                'label': 'Характеристики'}
                        },
                        {
                            'action': {
                                'type': 'text',
                                'label': 'Прокачать'}
                        },
                    ],
                    [
                        {
                            'action': {
                                'type': 'text',
                                'label': 'Назад 🔙'},
                            'color': 'negative'
                        },
                    ],
                ], }
car_keyboard = json.dumps(car_keyboard)

upgrade_keyboard = {"one_time": True,
                    "buttons": [
                        [
                            {
                                'action': {
                                    'type': 'text',
                                    'label': 'М. скорость'}
                            },
                            {
                                'action': {
                                    'type': 'text',
                                    'label': 'Ускорение'}
                            },
                            {
                                'action': {
                                    'type': 'text',
                                    'label': 'Турбо'}
                            },
                        ],
                        [
                            {
                                'action': {
                                    'type': 'text',
                                    'label': 'Назад 🔙'},
                                'color': 'negative'
                            },
                        ],
                    ], }
upgrade_keyboard = json.dumps(upgrade_keyboard)

profile_keyboard = {"one_time": True,
                    "buttons": [
                        [
                            {
                                'action': {
                                    'type': 'text',
                                    'label': 'Обо мне'}
                            },
                            {
                                'action': {
                                    'type': 'text',
                                    'label': 'Последние заезды'}
                            },
                        ],
                        [
                            {
                                'action': {
                                    'type': 'text',
                                    'label': 'Назад 🔙'},
                                'color': 'negative'
                            },
                        ],
                    ], }
profile_keyboard = json.dumps(profile_keyboard)

keyboards = {0: main_keyboard,
             1: race_keyboard,
             2: cancel_keyboard,
             3: clear_keyboard,
             4: back_keyboard,
             5: car_keyboard,
             6: upgrade_keyboard,
             7: profile_keyboard,
             8: exit_keyboard}
