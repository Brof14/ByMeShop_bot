from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message
from config import config
from database.database import AsyncSessionLocal
from database.models import Order, OrderStatus
from keyboards.inline import cancel_kb, games_kb, main_kb, payment_kb, so2_kb
from utils.states import BuySO2Gold, BuyTGStars

router = Router()


async def render_screen(call: CallbackQuery, photo_url: str, text: str, reply_markup):
    """Единая функция для красивого переключения экранов без спама."""
    try:
        await call.message.edit_media(
            media=InputMediaPhoto(media=photo_url, caption=text, parse_mode="HTML"),
            reply_markup=reply_markup,
        )
    except Exception as e:
        # Если фото не поменялось или возникла ошибка
        await call.message.edit_caption(
            caption=text, reply_markup=reply_markup, parse_mode="HTML"
        )


@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    text = "<b>Главное меню ByMeShop</b>\n──────────────────────\nДобро пожаловать! Выберите нужный раздел:"
    await message.answer_photo(
        photo=config.IMG_MAIN, caption=text, reply_markup=main_kb(), parse_mode="HTML"
    )


@router.callback_query(F.data == "cancel_action")
@router.callback_query(F.data == "main_menu")
async def back_to_main(call: CallbackQuery, state: FSMContext):
    await state.clear()
    text = (
        "<b>Главное меню ByMeShop</b>\n──────────────────────\nВыберите нужный раздел:"
    )
    await render_screen(call, config.IMG_MAIN, text, main_kb())


@router.callback_query(F.data == "cat_games")
async def show_games(call: CallbackQuery):
    text = "<b>Игры</b>\n──────────────────────\nВыберите игру для покупки:"
    await render_screen(call, config.IMG_GAMES, text, games_kb())


@router.callback_query(F.data == "game_so2")
async def show_so2(call: CallbackQuery):
    text = "<b>Standoff 2</b>\n──────────────────────\nВыберите тип товара:"
    await render_screen(call, config.IMG_SO2, text, so2_kb())


# --- Логика покупки Standoff 2 Голды ---
@router.callback_query(F.data == "so2_gold")
async def so2_gold_start(call: CallbackQuery, state: FSMContext):
    text = (
        "<b>Покупка Голды (Standoff 2)</b>\n"
        "──────────────────────\n"
        "Введите количество голды, которое хотите купить.\n"
        "<i>Минимум: <code>50</code> голды. Цена: <code>0.5 руб</code> за 1 шт.</i>"
    )
    await render_screen(call, config.IMG_SO2, text, cancel_kb("game_so2"))
    await state.set_state(BuySO2Gold.amount)


@router.message(BuySO2Gold.amount)
async def so2_gold_process(message: Message, state: FSMContext, bot: Bot):
    await message.delete()  # Удаляем сообщение пользователя для чистоты

    if not message.text.isdigit() or int(message.text) < 50:
        msg = await message.answer("❌ Ошибка! Введите число от 50.")
        return

    amount = int(message.text)
    price = amount * 0.5

    # Создаем заказ в БД
    async with AsyncSessionLocal() as session:
        new_order = Order(
            user_id=message.from_user.id,
            product_name=f"SO2 Голда x{amount}",
            amount=price,
        )
        session.add(new_order)
        await session.commit()
        order_id = new_order.id

    text = (
        f"<b>Счет на оплату</b>\n"
        f"──────────────────────\n"
        f"📦 Товар: <code>Standoff 2 — {amount} Голды</code>\n"
        f"🧾 Заказ ID: <code>{order_id}</code>\n"
        f"💰 К оплате: <code>{price} руб.</code>\n\n"
        f"<i>После успешной оплаты нажмите кнопку проверки.</i>"
    )
    # Отправляем новый экран оплаты
    await message.answer_photo(
        photo=config.IMG_SO2,
        caption=text,
        reply_markup=payment_kb(order_id),
        parse_mode="HTML",
    )
    await state.clear()


# --- Пример обработки кнопки проверки оплаты ---
@router.callback_query(F.data.startswith("check_pay_"))
async def check_payment(call: CallbackQuery, bot: Bot):
    order_id = int(call.data.split("_")[2])

    # Здесь должен быть реальный запрос к YooKassa/CryptoBot API
    # Для примера имитируем успешную оплату:
    is_paid = True

    if is_paid:
        async with AsyncSessionLocal() as session:
            order = await session.get(Order, order_id)
            order.status = OrderStatus.PAID
            await session.commit()

        success_text = (
            f"✅ <b>Заказ <code>{order_id}</code> успешно оплачен!</b>\n"
            f"──────────────────────\n"
            f"💬 После оплаты с вами свяжется поддержка ByMeShop и выполнит ваш заказ."
        )
        await render_screen(call, config.IMG_SERVICES, success_text, cancel_kb())

        # Уведомление админам
        for admin_id in config.ADMIN_IDS:
            try:
                await bot.send_message(
                    admin_id,
                    f"🔥 <b>Новый оплаченный заказ!</b>\nID: <code>{order_id}</code>\nТовар: {order.product_name}",
                    parse_mode="HTML",
                )
            except:
                pass
    else:
        await call.answer(
            "Оплата еще не поступила. Подождите пару минут.", show_alert=True
        )
