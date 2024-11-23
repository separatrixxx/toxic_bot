import json


# Файл для хранения рейтингов токсичности
RATINGS_FILE = '/data/toxicity_ratings.json'

# Загрузка рейтингов из файла
def load_ratings():
    try:
        with open(RATINGS_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Сохранение рейтингов в файл
def save_ratings(ratings):
    with open(RATINGS_FILE, 'w') as file:
        json.dump(ratings, file)

# Обработка команды +tox
def handle_tox_command(event, vk, send_message):
    toxicity_ratings = load_ratings()  # Загружаем рейтинги
    if 'reply_message' in event.message:
        reply_message = event.message['reply_message']
        target_id = str(reply_message['from_id'])  # Приводим ID к строке для консистентности
        
        # Увеличиваем рейтинг токсичности
        if target_id in toxicity_ratings:
            toxicity_ratings[target_id] += 1
        else:
            toxicity_ratings[target_id] = 1
        save_ratings(toxicity_ratings)

        # Получаем имя и фамилию пользователя
        user_info = vk.users.get(user_ids=target_id)
        if user_info:
            user_name = f"{user_info[0]['first_name']} {user_info[0]['last_name']}"
            send_message(event.message['peer_id'], f"Уровень токсичности {user_name} увеличен: {toxicity_ratings[target_id]}.")
    else:
        send_message(event.message['peer_id'], "Перешлите сообщение человека для увеличения уровня токсичности.")

# Обработка команды для вывода топа токсичных
def handle_tox_top_command(event, vk, send_message):
    toxicity_ratings = load_ratings()  # Загружаем рейтинги перед обработкой топа
    sorted_ratings = sorted(toxicity_ratings.items(), key=lambda x: x[1], reverse=True)
    top_list = []

    for rank, (user_id, rating) in enumerate(sorted_ratings, start=1):
        user_info = vk.users.get(user_ids=user_id)
        if user_info:
            user_name = f"{user_info[0]['first_name']} {user_info[0]['last_name']}"
            top_list.append(f"{rank}. {user_name}, {rating} очков")

    if top_list:
        send_message(event.message['peer_id'], "\n".join(top_list))
    else:
        send_message(event.message['peer_id'], "Список токсичности пуст.")
