import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from config import TOKEN, GROUP_ID
import toxics
import gays
import nyash
import schiz


# Инициализация API
vk_session = vk_api.VkApi(token=TOKEN)
longpoll = VkBotLongPoll(vk_session, GROUP_ID)
vk = vk_session.get_api()

# Функция для отправки сообщений
def send_message(peer_id, message):
    vk.messages.send(peer_id=peer_id, message=message, random_id=0)

# Возможные команды для вывода топов
tox_top_commands = {'список токсиков', 'получить токсиков', 'топ токсиков'}
gay_top_commands = {'список геев', 'получить геев', 'топ геев'}
nyash_top_commands = {'список няшек', 'получить няшек', 'топ няшек'}
schiz_top_commands = {'список шизов', 'получить шизов', 'топ шизов'}

# Основной цикл для обработки событий
for event in longpoll.listen():
    try:
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
            message_text = event.message['text'].lower()
            
            # Обработка команд для токсичности
            if message_text == '+tox' or message_text == '+токс':
                toxics.handle_tox_command(event, vk, send_message)
            elif message_text in tox_top_commands:
                toxics.handle_tox_top_command(event, vk, send_message)
            
            # Обработка команд для "геев"
            elif message_text == '+gay' or message_text == '+гей':
                gays.handle_gay_command(event, vk, send_message)
            elif message_text in gay_top_commands:
                gays.handle_gay_top_command(event, vk, send_message)

            # Обработка команд для "няшек"
            elif message_text == '+nyash' or message_text == '+няш':
                nyash.handle_nyash_command(event, vk, send_message)
            elif message_text in nyash_top_commands:
                nyash.handle_nyash_top_command(event, vk, send_message)

            # Обработка команд для "шизов"
            elif message_text == '+schiz' or message_text == '+шиз':
                schiz.handle_schiz_command(event, vk, send_message)
            elif message_text in schiz_top_commands:
                schiz.handle_schiz_top_command(event, vk, send_message)

    except Exception as e:
        print(f"Ошибка: {e}")
