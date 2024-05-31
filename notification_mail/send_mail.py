from data.database import get_mail_user


async def send_mail(email: str,  price: float) -> None:
    """
    Отправка сообщение в маил
    :param user_id:
    :param price:
    :return:
    """
    print('отправка маила', email)
