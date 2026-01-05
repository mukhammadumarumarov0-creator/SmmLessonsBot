from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


async def register_button(message: Message, text: str):
    """Ro'yhatdan o'tish tugmasini yuboradi"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📃 Ro'yhatdan o'tish")]],
        resize_keyboard=True
    )
    await message.answer(text=text, reply_markup=keyboard, parse_mode='HTML')

async def phone_button(message: Message, text: str):
    """Telefon raqam yuborish tugmasi"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📲 Raqam jo'natish", request_contact=True)]],
        resize_keyboard=True
    )
    await message.answer(text=text, reply_markup=keyboard, parse_mode='HTML')


def get_video_keyboard(lesson_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎬 Videoni ko‘rish",
                    callback_data=f"lesson:{lesson_id}:watch"
                )
            ]
        ]
    )

def get_next_keyboard(lesson_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⏭️ Keyingi",
                    callback_data=f"lesson:{lesson_id}:next"
                )
            ]
        ]
    )


btn_admin = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="👤 Admin bilan bog‘lanish")]],
    resize_keyboard=True
)

inline_kb = [
    [
        InlineKeyboardButton(
            text="✅ O'qib Chiqdim",
            callback_data="open_video_btn"
        )
    ]
]

btn = InlineKeyboardMarkup(inline_keyboard=inline_kb)
    
    