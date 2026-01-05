from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from asgiref.sync import sync_to_async
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from django.core.exceptions import ObjectDoesNotExist
import asyncio

from bot.instance.handlers.service import write_user_to_sheet_bg
from bot.models import Lesson, Test
from bot.instance.handlers.utils import (
    is_registered,
    create_user,
    validate_full_name,
    normalize_phone,
    update_user_is_watched_async,
    FULLNAME_ERROR,
    PHONE_ERROR
)
from .bottens import (
    register_button,
    phone_button,
    btn_admin,
    btn,
    get_video_keyboard,
    get_next_keyboard
)
from .messages import (
    congrats_message,
    ask_name_message,
    ask_phone_message,
    post_message,
    welcome_message,
    promo_message,
    pro_message,
    admin_connect,
    course_message
)

user_router = Router()

class RegisterProcess(StatesGroup):
    full_name = State()
    phone = State()



@user_router.message(CommandStart())
async def start_handler(message: types.Message):
    try:
        user = await is_registered(message.from_user.id)
    except Exception:
        await message.answer("❌ Tizim xatosi. Keyinroq urinib ko‘ring.")
        return

    meet_message = (
        f"Assalomu alaykum {message.from_user.first_name}! 👋\n\n"
        "Botdan to‘liq foydalanish uchun avvalo «Ro‘yxatdan o‘tish» tugmasini bosing ✅"
    )

    if user:
        await message.answer(welcome_message, reply_markup=btn_admin)
        first_lesson = await sync_to_async(lambda: Lesson.objects.order_by("id").first())()
        if first_lesson:
            await message.answer(
                pro_message,
                parse_mode="HTML",
                reply_markup=get_video_keyboard(first_lesson.id)
            )
    else:
        await register_button(message, meet_message)



@user_router.message(F.text == "👤 Admin bilan bog‘lanish")
async def admin_btn_handler(message: types.Message):
    await message.answer(
        admin_connect,
        parse_mode="HTML",
        disable_web_page_preview=True
    )



@user_router.message(F.text == "📃 Ro'yhatdan o'tish")
async def start_register(message: types.Message, state: FSMContext):
    await state.set_state(RegisterProcess.full_name)
    await message.answer(ask_name_message, parse_mode="HTML")



@user_router.message(RegisterProcess.full_name)
async def fullname_register(message: types.Message, state: FSMContext):
    if not message.text or not await validate_full_name(message.text):
        await message.answer(FULLNAME_ERROR, parse_mode="HTML")
        return

    await state.update_data(full_name=message.text)
    await state.set_state(RegisterProcess.phone)
    await phone_button(message, ask_phone_message)



@user_router.message(RegisterProcess.phone)
async def phone_register(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else message.text
    if not phone:
        await message.answer(PHONE_ERROR, parse_mode="HTML")
        return

    normalized = await normalize_phone(phone)
    if not normalized:
        await message.answer(PHONE_ERROR, parse_mode="HTML")
        return

    data = await state.get_data()
    await create_user(
        full_name=data.get("full_name"),
        phone=normalized,
        chat_id=message.from_user.id,
        username=message.from_user.username
    )

    # Google Sheets yozish (async)
    try:
        asyncio.create_task(write_user_to_sheet_bg(
            chat_id=message.from_user.id,
            username=message.from_user.username or "",
            full_name=data.get("full_name"),
            phone=normalized
        ))
    except Exception as e:
        print("Google Sheets error:", e)

    # Tabrik xabari
    don_message = (
        f"🎉 Tabriklaymiz, <b>{message.from_user.first_name}</b>!\n"
        "<b>✅ Ro‘yxatdan muvaffaqiyatli o‘tdingiz!</b>\n\n"
        "Endi siz botimizning barcha qulayliklaridan to‘liq foydalanishingiz mumkin va biz tayyorlagan\n"
        "<b>qiziqarli</b> hamda <b>foydali</b> video darsliklar orqali "
        "<b>300.000💰 so‘mlik vaucher</b> sohibi bo‘lish imkoniyatiga egasiz.\n\n"
        "<b>Inshalloh</b>, videolarimiz sizga <b>manfaatli va foydali</b> bo‘ladi.\n"
        "<b>Sizga omad tilaymiz!</b>\n\n"
        "⚡ Eslatma: Tez orada sizga <b>yana bir nechta qiziqarli postlar</b> keladi, kuzatib boring!"
    )


    

    await state.clear()
    await message.answer(don_message, parse_mode="HTML")
    await asyncio.sleep(12)
    await message.answer(course_message, parse_mode="HTML", reply_markup=btn_admin)
    await asyncio.sleep(10)
    try:
        media = InputMediaPhoto(media=FSInputFile("media/smm_intro.jpg"))
        await message.answer_media_group(media=[media])
    except Exception as e:
        print("Media yuborishda xato:", e)

    

    # 15 soniya kechikkan post
    await asyncio.sleep(20)
    await message.answer(text=post_message, parse_mode="HTML", reply_markup=btn)


# --------------------
# Callback: O'qib chiqdim
# --------------------
@user_router.callback_query(F.data == "open_video_btn")
async def lesson_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    first_lesson = await sync_to_async(lambda: Lesson.objects.order_by("id").first())()
    if first_lesson:
        await callback.message.answer(
            text=promo_message,
            parse_mode="HTML",
            reply_markup=get_video_keyboard(first_lesson.id)
        )
    else:
        await callback.message.answer("❌ Video topilmadi")


# --------------------
# Callback: Lesson watch/next
# --------------------
@user_router.callback_query(F.data.startswith("lesson:"))
async def lesson_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        _, lesson_id, action = callback.data.split(":")
        lesson_id = int(lesson_id)
    except ValueError:
        return

    try:
        lesson = await sync_to_async(lambda: Lesson.objects.select_related("video").get(id=lesson_id))()
    except ObjectDoesNotExist:
        await callback.message.answer("❌ Dars topilmadi")
        return

    if not lesson.video or not lesson.video.url:
        await callback.message.answer("❌ Video mavjud emas")
        return

    if action == "watch":

        await callback.answer()  # 👈 ENG MUHIM QATOR

        await callback.message.delete()
        await callback.message.answer_video(
            video=lesson.video.url,
            caption=(lesson.video.description or lesson.video.title)[:1000],
            reply_markup=get_next_keyboard(lesson.id)
        )
    elif action == "next":
        tests = await sync_to_async(lambda: list(lesson.tests.all()))()
        if not tests:
            await send_next_lesson(callback.message, lesson.id)
            return
        await callback.message.edit_reply_markup(reply_markup=None)
        await state.update_data(
            lesson_id=lesson.id,
            question_index=0,
            score=0,
            tests_ids=[t.id for t in tests]
        )
        await send_question(callback.message, state)



async def send_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if "lesson_id" not in data or "tests_ids" not in data:
        return

    index = data.get("question_index", 0)
    score = data.get("score", 0)
    tests_ids = data["tests_ids"]

    if index >= len(tests_ids):
        total = len(tests_ids)
        result_text = f"✅ Sizning Test Natijangiz : {score}/{total} \n\n"
        if score < total / 2:
            result_text += "⚠️ Afsuski Natijangiz past \n 😎 Lekin tashvishlanmang! \n 🚀Videoni qayta ko‘ring va yana urinib ko‘ring! \n"
            await message.answer(result_text)
            await asyncio.sleep(5)
            lesson = await sync_to_async(lambda: Lesson.objects.select_related("video").get(id=data["lesson_id"]))()
            if lesson.video and lesson.video.url:
                await message.answer_video(
                    video=lesson.video.url,
                    caption=(lesson.video.description or lesson.video.title)[:1000],
                    reply_markup=get_next_keyboard(lesson.id))
                
        else:
            if score == total :
                result_text += "🔥 Aqil bovar qilmaydi! \n 🌟 Juda yaxshi natija! Siz tug‘ma SMMchisiz 💪\n 🚀 Bilimlaringizni ishga soling va yangi cho‘qqilarni zabt eting! \n"
                await message.answer(result_text)
                await asyncio.sleep(5)
                await send_next_lesson(message, data["lesson_id"])
                return
            
            result_text += "👍 Yaxshi ishladingiz! \n 💥 Harakatlaringizni to‘xtatmang,\n 📊 SMM dunyosi sizdan katta natijalar kutmoqda! \n"
            await message.answer(result_text)
            await asyncio.sleep(5)
            await send_next_lesson(message, data["lesson_id"])

        await state.clear()
        return

    test_id = tests_ids[index]
    test = await sync_to_async(lambda: Test.objects.get(id=test_id))()

    buttons = [
        [types.InlineKeyboardButton(text=f"A) {test.option_a}", callback_data=f"ans:{index}:A")],
        [types.InlineKeyboardButton(text=f"B) {test.option_b}", callback_data=f"ans:{index}:B")]
    ]
    if test.option_c:
        buttons.append([types.InlineKeyboardButton(text=f"C) {test.option_c}", callback_data=f"ans:{index}:C")])
    if test.option_d:
        buttons.append([types.InlineKeyboardButton(text=f"D) {test.option_d}", callback_data=f"ans:{index}:D")])

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(test.question, reply_markup=keyboard)



@user_router.callback_query(F.data.startswith("ans:"))
async def answer_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        _, index, choice = callback.data.split(":")
        index = int(index)
    except ValueError:
        return

    data = await state.get_data()
    if index != data.get("question_index"):
        return

    test = await sync_to_async(lambda: Test.objects.get(id=data["tests_ids"][index]))()
    score = data.get("score", 0)
    if choice == test.correct_option:
        score += 1

    await state.update_data(score=score, question_index=index + 1)
    await send_question(callback.message, state)



async def send_next_lesson(message: types.Message, current_lesson_id: int):
    next_lesson = await sync_to_async(
        lambda: Lesson.objects.select_related("video")
        .filter(id__gt=current_lesson_id)
        .order_by("id")
        .first()
    )()
    if not next_lesson or not next_lesson.video:
        await message.answer(text=congrats_message,parse_mode="HTML")
        await update_user_is_watched_async(message.chat.id)
        return

    await message.answer_video(
        video=next_lesson.video.url,
        caption=(next_lesson.video.description or next_lesson.video.title)[:1000],
        reply_markup=get_next_keyboard(next_lesson.id)
    )
