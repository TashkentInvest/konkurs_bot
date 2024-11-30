import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.exceptions import ChatNotFound

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

API_TOKEN = '7888482179:AAHXGpLC-YUfMLRcC3ZK8eGnA0Wwx-SPsfI'  # Replace with your bot's token
CHANNEL_USERNAME = '@tik_konkurs'  # Replace with your channel's username (without @)

# Initialize the bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Function to check if a user is subscribed to the channel
async def is_subscribed(user_id: int) -> bool:
    try:
        logger.debug(f"Checking subscription for user ID: {user_id}")
        # Check the user's membership status in the channel
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        logger.debug(f"User {user_id} status in channel {CHANNEL_USERNAME}: {member.status}")
        
        if member.status in ['member', 'administrator', 'creator']:
            return True
        else:
            return False
    except ChatNotFound:
        logger.error(f"Channel {CHANNEL_USERNAME} not found or user {user_id} is not a member.")
        return False

# Handler for the "/start" command
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    start_param = message.get_args()  # Get the arguments passed in the start command

    logger.debug(f"Received /start command from user: {user_id}, with start param: {start_param}")
    
    if start_param == 'check_subscription':
        if await is_subscribed(user_id):
            # Send a message to the user if they are subscribed
            await bot.send_message(chat_id, "Сиз каналга обуна бўлдингиз! Мана сизга керакли контент.")
            
            # Content for the user
            image_url = "https://www.gazeta.uz/media/img/2024/08/sUj9DD17235359391151_b.jpg"
            text = (
                "Саломат\n\n"
                "Тошкентда тадбиркорлик ва шаҳар қурилиши учун 110 дан ортиқ ер участкалари E-auksion платформада сотувга қўйилди.\n\n"
                "2024-йил 13-август, 15:00   Жамият    Реклама\n\n"
                "Батафсил маълумотни қуйидаги ҳавола орқали олиш мумкин.\n\n"
                "Telegram: t.me/onlineauksionuz"
            )
            
            # Create inline button for the post content
            keyboard = InlineKeyboardMarkup()
            button = InlineKeyboardButton(text="E-auksionга ўтиш", url="https://t.me/tik_konkurs_bot?start=check_subscription")
            keyboard.add(button)

            # Add the new button with the link to the external site
            external_button = InlineKeyboardButton(text="Лойиҳани кўриш", url="https://projects.toshkentinvest.uz/")
            keyboard.add(external_button)
            
            try:
                # Send content directly to the user
                await bot.send_photo(
                    chat_id=chat_id,  # Send the content to the user's chat
                    photo=image_url, 
                    caption=text, 
                    reply_markup=keyboard
                )
                logger.info("Махсус контент фойдаланувчига юборилди.")
            except Exception as e:
                logger.error(f"Махсус контентни фойдаланувчига юборишда хато: {e}")
        else:
            # Prompt the user to subscribe to the channel if not subscribed
            await bot.send_message(chat_id, "Сиз контентни олиш учун каналга обуна бўлишингиз керак.")
            keyboard = InlineKeyboardMarkup()
            subscribe_button = InlineKeyboardButton(text="Каналга обуна бўлиш", url=f'https://t.me/tik_konkurs')
            keyboard.add(subscribe_button)
            await bot.send_message(chat_id, "Каналга обуна бўлиш учун қуйидаги тугмани босинг.", reply_markup=keyboard)
    else:
        await bot.send_message(chat_id, "Хуш келибсиз! Сўнгги контентимизни текшириш учун қуйидаги тугмани босинг: https://t.me/tik_konkurs")

# Handler for the "/subscribe" command (optional)
@dp.message_handler(commands=['subscribe'])
async def subscribe_command(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if await is_subscribed(user_id):
        await bot.send_message(chat_id, "Сиз аллақачон каналга обуна бўлдингиз!")
    else:
        # Send the user the link to the channel so they can subscribe
        await bot.send_message(chat_id, f"Каналга обуна бўлиш учун [бу ерга](https://t.me/tik_konkurs) босинг.")

# Handler for the "/post" command
@dp.message_handler(commands=['post'])
async def post_content(message: types.Message):
    # Only allow admins to send posts (or any specific user)
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Here you can define the post content
    image_url = "https://www.gazeta.uz/media/img/2024/08/sUj9DD17235359391151_b.jpg"  # Example image URL
    text = (
        "Тошкентда 110 дан ортиқ ер участкалари E-auksionда сотувга қўйилди.\n\n"
        "Бизнинг платформамизда сиз осонлик билан ариза беришингиз мумкин.\n\n"
        "Янги лойиҳаларни кўриш учун қуйидаги ҳаволани босинг."
    )

    # Create an inline button for the post content
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="E-auksionга ўтиш", url="https://t.me/tik_konkurs_bot?start=check_subscription")
    keyboard.add(button)

    # Add an external link button
    external_button = InlineKeyboardButton(text="Лойиҳани кўриш", url="https://projects.toshkentinvest.uz/")
    keyboard.add(external_button)
    
    try:
        # Send the content to the channel
        await bot.send_photo(
            chat_id=CHANNEL_USERNAME,  # Post to the channel (replace with your channel's username)
            photo=image_url, 
            caption=text, 
            reply_markup=keyboard  # Attach the inline keyboard
        )
        logger.info("Пост с расм, матн ва тугмалар билан каналга юборилди.")
        await bot.send_message(chat_id, "Сизнинг постингиз муваффақиятли каналга юборилди!")
    except Exception as e:
        logger.error(f"Постингиз юборишда хато юз берди: {e}")
        await bot.send_message(chat_id, "Постингиз юборишда хато юз берди. Илтимос, қўйидаги тугмани қайтадан босинг.")

# Start polling (this will start the bot)
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
