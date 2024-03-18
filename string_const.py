# Файл для строковых констант оформления
from string import Template
import config

DISCONNECT_BTN_TEXT = '🔚 Отключиться'
EXIT_BTN_TEXT = '🚪 Выйти'
STOP_SEARCH_BTN_TEXT = '🛑 Стоп'
START_SEARCH_BTN_TEXT = '🔍 Найти собеседника'
HELP_BTN_TEXT = '⁉️ Помощь'
VIP_BTN_TEXT = '👑 V.I.P.'
REFERRAL_PROGRAM_BTN_TEXT = '🔗 Реферальная программа'
SUPPORT_BTN_TEXT = '🤝 Поддержать проект'
PROFILE_BTN_TEXT = '👤 Профиль'
ABOUT_BOT_BTN_TEXT = 'ℹ️ О боте'


ADVERTISING_CONTACT_LINK = 'https://t.me/D_smm'


START_TEXT = \
"""<b>Привет! Это анонимный чат-бот города Алатырь.</b>

Здесь ты можешь общаться, делиться опытом и находить новых знакомых, сохраняя при этом анонимность 🎭
А ещё тут можно найти свою вторую половинку 💞

<i>Присоединяйся к нашим социальным сетям, чтобы быть в курсе всех новостей проекта 📰</i>
<a href=\"https://vk.com/anonymousalatyr\">Сообщество ВКонтакте</a>
<a href=\"https://t.me/AnonymousAlatyr\">Telegram канал</a>"""
START_COMMAND_TEXT = \
"""<i><a href=\"http://t.me/AnonymousAlatyr_support_bot\">Поддержка</a> - решит ваши проблемы</i>
<i><a href=\"http://t.me/AnonymousAlatyr_feedback_bot\">Обратная связь</a> - ваши предложения</i>"""

SEARCH_STOPED = 'Поиск остановлен'
CONNECTED_TEXT = 'Собеседник найден!'
PARTNER_DISCONNECTED_TEXT = 'Собеседник завершил диалог :('
YOU_DISCONNECTED_TEXT = 'Вы завершили диалог.'
YOU_NOT_CONNECTED_TEXT = 'Вы не подключены к чату!'
SEARCH_PARTNER_TEXT = 'Ожидайте, скоро найдем вам кого нибудь :)'

HELP_TEXT = 'Комманды бота:\n\n' \
			'/start - главное меню\n' \
			'/search - найти собеседника\n' \
			'/profile - профиль\n' \
			'/rating - рейтинг меню\n' \
			'/info - информация'

NOT_REGISTER_WITH_YOUR_LINK_TEXT = "Нельзя регистрироваться по своей реферальной ссылке."
# <i>Чем выше рейтинг, тем выше твоё место!</i> 
# <i>Чем больше у тебя рефералов, тем выше твоё место!</i> 
ABOUT_BOT_TEXT = \
"""
<b>🔸 Анонимный Алатырь</b>

<u><b>🏆 Система рейтингов</b></u>
Каждому новому пользователю мы даём 10 очков рейтинга. После диалога собеседник ставит вам одну из оценок 👍 или 👎. Этот отзыв повышает или понижает ваш рейтинг.

<u><b>🔗 Реферальная программа</b></u>
Отправьте вашу реферальную ссылку друзьям и знакомым. Расскажите об Анонимном Алатыре в вашем интернет блоге.

<s><b>💰 Платная подписка</b></s>
Мы решили не добавлять платные подписки, чтобы все пользователи чувствовали себя одинаково хорошо. Однако вы всё равно можете нас поддержать. Один из способов — приобрести рекламу в нашем боте.

<u><b>Вы можете отправлять 👌</b></u>
┣ Текстовые сообщения
┣ Голосовые сообщения
┣ Аудио файлы
┣ Фотографии
┣ Кружочки
┣ Стикеры
┗ Видео

<u><b>В чате запрещены 🚫</b></u>
┣ Угрозы
┣ Реклама
┣ Оскорбления
┗ Материалы 18+

<b>© Сделано в Алатыре!</b>"""
YOUR_REFERRAL_REGISTERED_TEXT = '🔗 По вашей реферальной ссылке зарегистрировался новый пользователь.'

LEAVE_OPINION_TEXT = 'Как прошёл ваш диалог?'
MUT_TEXT = """На вас много жалуются. В связи с этим мы приняли решение отправить вас в MUT. 

Если вы не согласны с нашим решением, напишите в поддержку. <a href=\"http://t.me/AnonymousAlatyr_support_bot/">📞 ПОДДЕРЖКА</a>

Cтатус и время до окончания MUT можно посмотреть в своём профиле."""

PARDON_TEXT = "⚖️ Совет модераторов принял решение снять с вас MUT. Просим прощения за доставленные неудобства."
COMPLAIN_CAUSE_SEND_ALERT_TEXT = 'Жалоба на пользователя отправлена. Мы сожалеем о случившемся :('

SUPPORT_TEXT = \
f"""В качестве поддержки вы можете приобрести рекламу в нашем боте. 
<i>По рекламе ➡️ @{config.ADVERTISING_MANAGER}</i>

или

Простой перевод по номеру карты <i>(нажмите, чтобы скопировать)</i>
СберБанк: <code>{config.SBERBANK}</code>
Тинькофф: <code>{config.TINKOFF}</code>
Денис Александрович Д."""

ADMIN_HELP_TEXT = """
Админка:
/help
/sendall
/get_db_users
/get_db_history
/get_db_queue
<code>/minus_complaint</code>
<code>/add_rating</code> user_id
<code>/minus_rating</code> user_id quantity
<code>/add_referral</code> user_id
<code>/minus_referral</code> user_id rating
<code>/set_status user_id FREE</code>  
<code>/set_status user_id MUT time</code>"""

PROFILE_TEMPLATE = Template(f'Статуст - <b>$status</b> $status_description\n\n' \
                           f'🏆 Ваш рейтинг <b>$rating</b>\n' \
                           f'📊 Вы на <b>$rating_place</b> месте по рейтингу.\n\n' \
                           f'👥 У вас <b>$referral</b> рефералов\n' \
                           f'📊 Вы на <b>$referral_place</b> месте по числу рефералов.\n\n<i>Нажмите <b>`{ABOUT_BOT_BTN_TEXT}`</b>, чтобы узнать как увеличить свой рейтинг и прифлечь рефералов.</i>')

DOWN_RATING_TEMPLATE = Template("""Уважаемый пользователь, модераторы обнаружили некоторые нечестные методы накрутки вашего рейтинга, что вызвало подозрения в его честности. <b>В качестве штрафа мы убавим ваш рейтинг на $quantity единиц.</b> 

Если вы не согласны с нашим решением, напишите в поддержку. <a href=\"http://t.me/AnonymousAlatyr_support_bot/">📞 ПОДДЕРЖКА</a>

Рейтинг можно посмотреть в своём профиле.""")


REFERRAL_PROGRAM_TEMPLATE = Template(f'Ваша реферальная ссылка:\n<code>$ref_link</code>\n\nОтправьте её друзьям. Все кто передут по ней станут вашими рефералами.\n\n<i>Количество ваших рефералов можно посмотреть тут <b>`{PROFILE_BTN_TEXT}`</b></i>')

NEW_REFERRAL_USER_TEMPLATE = Template('<code>$user_id</code> зарегистрировался по реферальной ссылке <code>$referral_id<code>\n\n#REFERRAL')
MUT_MODERATION_TEMPLATE = Template('<code>$user_id</code> получил мут на $mut_time часов.\n\n#MUT')
FREE_MODERATION_TEMPLATE = Template('<code>$admin_id</code> снял мут с <code>$user_id</code>\n\n#FREE')
ADD_VIOLATION_TEMPLATE = Template('<code>$user_id</code> нарушил правила.\n\n#VIOLATION')
POTENTIAL_SPONSOR_TEMPLATE = Template('<code>$user_id</code> - потенциально спонсор.\n\n#SPONSOR')
SUSPECTS_RATING_CHEATING_TEMPLATE = Template('<code>$user_id</code> снова ставит <code>$partner_id</code> хорошую оценку.\n\n#RC_SUSPECT')

# SHARE_PROFILE = '👤 Поделиться профилем'
# # Ответы на комманды
# WELCOME_TEXT = 'Привет!\n\n' \
# 			   'Это анонимный чат бот Chatium😎\n\n' \
# 			   'Тут ты можешь найти себе новых друзей или пообщаться со старыми :)\n' \
# 			   'Заходи в наш телеграм канал чтобы быть в курсе всех новостей нашего проекта 💖\n\n' \
# 			   'Chatium Community - @chatium_community'

# HELP_TEXT = 'Комманды бота:\n\n' \
# 			'/start - главное меню\n' \
# 			'/search - найти собеседника\n' \
# 			'/profile - профиль\n' \
# 			'/rating - рейтинг меню\n' \
# 			'/info - информация'
# INFORMATION_TEXT = 'ℹ️ <b>Информация</b>'
# # FIX IT
# SUPPORT_INFO_TEXT = '<b>Поддержи проект!</b>'

# # Кнопки мейн меню
# SEARCH_TEXT = '🔍 Поиск'
# RATING_TEXT = '⭐️ Рейтинг'
# PROFILE_TEXT = '👤 Профиль'
# INFO_TEXT = 'ℹ️ Информация'

# # Кнопки второстепенных меню
# SEND_BUG_REPORT_TEXT = '🐞 Отправить баг репорт'
# HELP_LINK_TEXT = '🧰 Помощь'
# SUPPORT_TEXT = '😉 Поддержать проект'

# # Баг репорт тексты
# SEND_BUG_REPORT_WELCOME_TEXT = 'Очень приятно что вы помогаете нашему проекту развиваться 💘\n\n' \
# 							   'Опишите баг который вы лицезрели, максимально подробно, это важно\n' \
# 							   'Если есть возможность укажите время когда баг произошёл'
# SEND_BUG_REPORT_IMAGE = 'Прекрасно!\n\n' \
# 						'Теперь отправьте скриншот произошедшего бага\n' \
# 						'Ещё раз спасибо за содействие в улучшении проекта 🙂'
# THANKS_FOR_BUG_REPORT_TEXT = 'Спасибо за баг репорт!\n' \
# 							 'Мы обязательно его пофиксим'

# # Темплейты
# PROFILE_TEMPLATE = Template('Профиль\n\n' \
# 							'🔎 ID: $id\n' \
# 							'📅 Ты с нами $days д. $hours ч. \n' \
# 							'⭐️ Очков рейтинга - $rating_score\n' \
# 							'$additional_info\n'
# 							'✉️ Всего отправленных сообщений: $count_messages\n' \
# 							'👤 Начато диалогов: $count_dialogs')
# RATING_TEMPLATE = Template('Рейтинг самых п#здатых в этом чат боте😎\n' \
# 						   'Очки рейтинга получаются с помощью активностей в боте\n\n$users_rating')
# ADMIN_TEMPLATE = Template('Привет!\nЭто админ меню')
# SCAM_TEMPLATE = 'Вас пытаются обмануть!\n' \
# 				'Человек попытался отправить фейковую монетку не тут-то было....\n\n' \
# 				'P.S Chatium :)'

# # Кнопки админки
# DISTRIBUTION_TEXT = '✉️ Рассылка'
# SWITCH_TO_USER_MODE_TEXT = 'Перейти в админ режим'

# # Кнопки чатинга
# STOP_TEXT = 'Стоп 🛑'
# SHARE_LINK_TEXT = 'Поделиться ссылкой 📨'
# SHARE_LINK_TEMPLATE = Template('Пользователь поделился с тобой ссылкой - t.me/$username')
# DIALOG_END = 'Диалог закончен :('
# WAIT_MORE_2_SEC_TEXT = 'Ожидайте, скоро найдем вам кого нибудь:)'
# START_SEARCH = '<i>Поиск...</i>'
# END_SEARCH = 'Собеседник найден!'
# COIN_FLIP_TEXT = 'Монетка 🪙'
# COIN_FLIP_TEMPLATE = Template('Вам выпал $coin_flip 🪙')
# ALREADY_SEARCH_TEXT = 'Мы уже ищем вам собеседника!'
# NEXT_COMPANION_TEXT = 'Следующий ➡️'
# EXIT_TEXT = 'Выйти ◀️'
# QUIT_FROM_QUEUE = 'Мы не нашли вам никого :('
# NOBODY_FOUND = 'Никого тебе не нашли😔\nЗаглядывай попозже'

# TECH_PAUSE = 'Технический перерыв 😔\n' \
# 			 'Возвращайтесь позже, бот станет ещё лучше :)'# TECH_PAUSE = 'Технический перерыв 😔\n' \
# 			 'Возвращайтесь позже, бот станет ещё лучше :)'# 			 'Возвращайтесь позже, бот станет ещё лучше :)'# 			 'Возвращайтесь позже, бот станет ещё лучше :)'# TECH_PAUSE = 'Технический перерыв 😔\n' \
# 			 'Возвращайтесь позже, бот станет ещё лучше :)'# 			 'Возвращайтесь позже, бот станет ещё лучше :)'