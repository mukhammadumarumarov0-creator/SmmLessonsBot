import re
from asgiref.sync import sync_to_async
from bot.models import User, Lesson

# =========================
# Sync helpers
# =========================
def get_user_sync(chat_id: int) -> User | None:
    return User.objects.filter(chat_id=chat_id).first()

def update_user_watched_sync(chat_id: int, lesson_id: int = None) -> User | None:
    user = User.objects.filter(chat_id=chat_id).first()
    if not user:
        return None

    user.is_watched = True
    user.save()
    return user


# =========================
# Async wrappers
# =========================
async def is_registered(chat_id: int) -> User | None:
    return await sync_to_async(get_user_sync)(chat_id)


async def create_user(full_name: str, phone: str, chat_id: int,username : str) -> User:
    return await sync_to_async(User.objects.create)(
        full_name=full_name, phone=phone, chat_id=chat_id,username=username
    )



# =========================
# Validators
# =========================
FULLNAME_ERROR = (
    "❌ Ism va familiyani to‘g‘ri kiriting.\n"
    "Masalan: Muhammad Umarov"
)

PHONE_ERROR = (
    "❌ Telefon raqam noto‘g‘ri.\n"
    "Namuna: +998901234567\n"
    "Yoki 📞 tugmani bosing"
)


async def validate_full_name(full_name: str) -> bool:
    """
    Format: 'Ism Familiya' (2-30 harf, Lotin va Kirill)
    """
    FULL_NAME_REGEX = r"^[A-Za-zА-Яа-яЎўҚқҒғҲҳЁё]{2,30}\s[A-Za-zА-Яа-яЎўҚқҒғҲҳЁё]{2,30}$"
    return bool(re.fullmatch(FULL_NAME_REGEX, full_name.strip()))


async def normalize_phone(phone: str) -> str | None:
    """
    Normalize: +998901234567 formatiga keltirish
    """
    PHONE_REGEX = r"^\+998(90|91|93|94|95|97|98|99|33|88)\d{7}$"
    digits = re.sub(r"\D", "", phone)

    if digits.startswith("998") and len(digits) == 12:
        digits = "+" + digits
    elif digits.startswith("9") and len(digits) == 9:
        digits = "+998" + digits
    else:
        return None

    return digits if re.fullmatch(PHONE_REGEX, digits) else None


def update_is_completed_by_chat_id(chat_id):
    user = User.objects.filter(chat_id=chat_id).first()
    if user:
        user.is_watched = True
        user.save() 
        return user
    return None


async def update_user_is_watched_async(chat_id):
    return await sync_to_async(update_is_completed_by_chat_id)(chat_id)


    
