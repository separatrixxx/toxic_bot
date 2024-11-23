import json


# Файл для хранения рейтингов "геев"
GAY_RATINGS_FILE = '/data/gay_ratings.json'

# Загрузка рейтингов из файла
def load_ratings():
    try:
        with open(GAY_RATINGS_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Сохранение рейтингов в файл
def save_ratings(ratings):
    with open(GAY_RATINGS_FILE, 'w') as file:
        json.dump(ratings, file)

# Обработка команды +gay
def handle_gay_command(event, vk, send_message):
    gay_ratings = load_ratings()  # Загружаем актуальные рейтинги
    if 'reply_message' in event.message:
        reply_message = event.message['reply_message']
        target_id = str(reply_message['from_id'])  # Приводим ID к строке для консистентности
        
        # Увеличиваем рейтинг "геев"
        if target_id in gay_ratings:
            gay_ratings[target_id] += 1
        else:
            gay_ratings[target_id] = 1
        
        # Сохраняем обновленный рейтинг
        save_ratings(gay_ratings)

        # Получаем имя и фамилию пользователя
        user_info = vk.users.get(user_ids=target_id)
        if user_info:
            user_name = f"{user_info[0]['first_name']} {user_info[0]['last_name']}"
            send_message(event.message['peer_id'], f"Уровень гейства {user_name} увеличен: {gay_ratings[target_id]}.")
    else:
        send_message(event.message['peer_id'], "Перешлите сообщение человека для увеличения уровня гейства.")

# Обработка команды для вывода топа "геев"
def handle_gay_top_command(event, vk, send_message):
    gay_ratings = load_ratings()  # Загружаем рейтинги перед обработкой топа
    sorted_ratings = sorted(gay_ratings.items(), key=lambda x: x[1], reverse=True)
    top_list = []

    for rank, (user_id, rating) in enumerate(sorted_ratings, start=1):
        user_info = vk.users.get(user_ids=user_id)
        if user_info:
            user_name = f"{user_info[0]['first_name']} {user_info[0]['last_name']}"
            top_list.append(f"{rank}. {user_name}, {rating} очков")

    if top_list:
        send_message(event.message['peer_id'], "\n".join(top_list))
    else:
        send_message(event.message['peer_id'], "Список геев пуст.")
