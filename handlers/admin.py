from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from config import config
from database.database import AsyncSessionLocal
from database.models import Product
from utils.states import AdminAddProduct

router = Router()


# Проверка на админа через фильтр
def is_admin(user_id: int) -> bool:
    return user_id in config.ADMIN_IDS


@router.message(F.text == "/admin", F.from_user.id.in_(config.ADMIN_IDS))
async def admin_panel(message: Message):
    text = "<b>Админ Панель</b>\n──────────────────────\nДля добавления товара введите /add_product"
    await message.answer(text, parse_mode="HTML")


@router.message(F.text == "/add_product", F.from_user.id.in_(config.ADMIN_IDS))
async def add_product_start(message: Message, state: FSMContext):
    await message.answer("Введите название товара:")
    await state.set_state(AdminAddProduct.name)


@router.message(AdminAddProduct.name)
async def add_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание товара:")
    await state.set_state(AdminAddProduct.desc)


@router.message(AdminAddProduct.desc)
async def add_desc(message: Message, state: FSMContext):
    await state.update_data(desc=message.text)
    await message.answer("Введите цену товара (число):")
    await state.set_state(AdminAddProduct.price)


@router.message(AdminAddProduct.price)
async def add_price(message: Message, state: FSMContext):
    try:
        price = float(message.text)
    except ValueError:
        return await message.answer("❌ Цена должна быть числом!")

    await state.update_data(price=price)
    await message.answer("Введите логин аккаунта (или '-' если не требуется):")
    await state.set_state(AdminAddProduct.login)


@router.message(AdminAddProduct.login)
async def add_login(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Введите пароль аккаунта (или '-'):")
    await state.set_state(AdminAddProduct.password)


@router.message(AdminAddProduct.password)
async def add_password(message: Message, state: FSMContext):
    data = await state.get_data()

    async with AsyncSessionLocal() as session:
        product = Product(
            name=data["name"],
            description=data["desc"],
            price=data["price"],
            login_data=message.text if message.text != "-" else None,
            password_data=data["login"] if data["login"] != "-" else None,
        )
        session.add(product)
        await session.commit()

    await message.answer("✅ Товар успешно добавлен в базу!")
    await state.clear()
