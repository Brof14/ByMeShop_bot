from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🎮 Игры", callback_data="cat_games")
    kb.button(text="📱 Telegram", callback_data="cat_tg")
    kb.button(text="🔌 Сервисы", callback_data="cat_services")
    kb.button(text="👤 Профиль", callback_data="cat_profile")
    kb.button(text="🛠 Поддержка", url="https://t.me/support")
    kb.adjust(2, 2, 1)
    return kb.as_markup()


def games_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🎯 Standoff 2", callback_data="game_so2")
    kb.button(text="👑 Brawl Stars", callback_data="game_bs")
    kb.button(text="☄️ PUBG Mobile", callback_data="game_pubg")
    kb.button(text="🧱 Roblox", callback_data="game_roblox")
    kb.button(text="💎 Free Fire", callback_data="game_ff")
    kb.button(text="🔙 Назад", callback_data="main_menu")
    kb.adjust(2, 2, 1, 1)
    return kb.as_markup()


def so2_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🟡 Голда", callback_data="so2_gold")
    kb.button(text="👤 Аккаунты", callback_data="so2_accs")
    kb.button(text="🔙 Назад", callback_data="cat_games")
    kb.adjust(2, 1)
    return kb.as_markup()


def cancel_kb(back_to: str = "main_menu") -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if back_to:
        kb.button(text="🔙 Назад", callback_data=back_to)
    kb.button(text="❌ Отмена", callback_data="cancel_action")
    kb.adjust(1)
    return kb.as_markup()


def payment_kb(order_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text="💳 Оплатить", url=f"https://yookassa.ru/pay/{order_id}"
    )  # Заглушка URL
    kb.button(text="🔄 Проверить оплату", callback_data=f"check_pay_{order_id}")
    kb.button(text="❌ Отменить", callback_data=f"cancel_order_{order_id}")
    kb.adjust(1)
    return kb.as_markup()
