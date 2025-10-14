from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import logging
logging.basicConfig(level=logging.INFO)

# === ВСТАВЬ СВОЙ ТОКЕН ЗДЕСЬ ===
BOT_TOKEN = "8026285248:AAF1oGQQGSsi0AAGzaBWs0tohSWpALUz27U"  # ← ЗАМЕНИ ЭТУ СТРОКУ НА СВОЙ ТОКЕН!

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class DesignQuiz(StatesGroup):
    goal = State()
    experience = State()
    platform = State()
    budget = State()
    teamwork = State()

GOALS = {
    "1": "Веб-сайты / UI/UX",
    "2": "Логотипы / иллюстрации",
    "3": "Презентации / соцсети",
    "4": "Фото / коллажи"
}

EXPERIENCE = {"1": "Новичок", "2": "Опытный"}
PLATFORMS = {"1": "Windows", "2": "Mac", "3": "Онлайн (браузер)"}
BUDGET = {"1": "Бесплатно", "2": "Готов платить"}
TEAMWORK = {"1": "Один", "2": "В команде"}

@dp.message_handler(commands=['start'])
async def start_quiz(message: types.Message):
    await DesignQuiz.goal.set()
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for k, v in GOALS.items():
        kb.add(f"{k}. {v}")
    await message.answer("🎨 Привет! Я помогу выбрать тебе идеальное приложение для дизайна.\n\n"
                         "Что ты хочешь создавать?", reply_markup=kb)

@dp.message_handler(state=DesignQuiz.goal)
async def process_goal(message: types.Message, state: FSMContext):
    key = message.text.split('.')[0] if '.' in message.text else None
    if key not in GOALS:
        await message.answer("Пожалуйста, выбери вариант из кнопок.")
        return
    await state.update_data(goal=key)
    await DesignQuiz.next()
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for k, v in EXPERIENCE.items():
        kb.add(f"{k}. {v}")
    await message.answer("Твой опыт в дизайне?", reply_markup=kb)

@dp.message_handler(state=DesignQuiz.experience)
async def process_experience(message: types.Message, state: FSMContext):
    key = message.text.split('.')[0] if '.' in message.text else None
    if key not in EXPERIENCE:
        await message.answer("Выбери из кнопок.")
        return
    await state.update_data(experience=key)
    await DesignQuiz.next()
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for k, v in PLATFORMS.items():
        kb.add(f"{k}. {v}")
    await message.answer("На какой платформе ты работаешь?", reply_markup=kb)

@dp.message_handler(state=DesignQuiz.platform)
async def process_platform(message: types.Message, state: FSMContext):
    key = message.text.split('.')[0] if '.' in message.text else None
    if key not in PLATFORMS:
        await message.answer("Выбери из кнопок.")
        return
    await state.update_data(platform=key)
    await DesignQuiz.next()
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for k, v in BUDGET.items():
        kb.add(f"{k}. {v}")
    await message.answer("Какой у тебя бюджет?", reply_markup=kb)

@dp.message_handler(state=DesignQuiz.budget)
async def process_budget(message: types.Message, state: FSMContext):
    key = message.text.split('.')[0] if '.' in message.text else None
    if key not in BUDGET:
        await message.answer("Выбери из кнопок.")
        return
    await state.update_data(budget=key)
    await DesignQuiz.next()
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for k, v in TEAMWORK.items():
        kb.add(f"{k}. {v}")
    await message.answer("Ты работаешь один или в команде?", reply_markup=kb)

@dp.message_handler(state=DesignQuiz.teamwork)
async def process_teamwork_and_recommend(message: types.Message, state: FSMContext):
    key = message.text.split('.')[0] if '.' in message.text else None
    if key not in TEAMWORK:
        await message.answer("Выбери из кнопок.")
        return
    await state.update_data(teamwork=key)
    data = await state.get_data()
    await state.finish()

    goal = data['goal']
    exp = data['experience']
    platform = data['platform']
    budget = data['budget']
    teamwork = data['teamwork']

    if goal == "3":
        recommendation = "🌟 **Canva** — идеально для новичков, бесплатная версия мощная, работает онлайн."
    elif goal == "1":
        if exp == "1":
            recommendation = "✨ **Figma** — бесплатна, онлайн, отлична для команды и новичков. Подходит для сайтов и интерфейсов."
        else:
            recommendation = "🚀 **Figma** или **Adobe XD** — Figma лучше для команды, XD — если ты в экосистеме Adobe."
    elif goal == "2":
        if budget == "1":
            recommendation = "🖌️ **Inkscape** (бесплатно) или **Vectr** — хороши для векторной графики. Но для профи — **Adobe Illustrator**."
        else:
            recommendation = "🖋️ **Adobe Illustrator** — золотой стандарт для логотипов и иллюстраций."
    elif goal == "4":
        if budget == "1":
            recommendation = "📸 **Photopea** (онлайн, как Photoshop) или **GIMP** — мощные бесплатные аналоги."
        else:
            recommendation = "🖼️ **Adobe Photoshop** — лучший выбор для фото и коллажей."
    else:
        recommendation = "🛠️ Попробуй **Figma** — универсальный и бесплатный инструмент для большинства задач!"

    if teamwork == "2" and "Figma" not in recommendation:
        recommendation += "\n\n💡 Но если работаешь в команде — подумай о **Figma**: она отлично поддерживает совместную работу!"

    if platform == "3":
        if "Figma" not in recommendation and "Canva" not in recommendation:
            recommendation += "\n\n🌐 Так как ты хочешь работать онлайн, обрати внимание на **Figma**, **Canva** или **Photopea**."

    await message.answer(
        f"✅ Готово! Исходя из твоих ответов:\n\n{recommendation}\n\nУдачи в творчестве! 🎨",
        parse_mode="Markdown",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await message.answer("Хочешь пройти опрос заново? Напиши /start")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)