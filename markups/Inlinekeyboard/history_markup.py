from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

markup_history_admin = InlineKeyboardMarkup()

markup_history_admin.row(InlineKeyboardButton('❌ В ожидании', callback_data='waiting[ADMIN]'), InlineKeyboardButton('✅ Принятые', callback_data='history[ADMIN]'))

markup_history = InlineKeyboardMarkup()

markup_history.row(InlineKeyboardButton('❌ В ожидании', callback_data='waiting'), InlineKeyboardButton('✅ Принятые', callback_data='history'))
