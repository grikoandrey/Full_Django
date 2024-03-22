from django.contrib.auth.models import Group  # импортирует модель Group, представляет группу пользователей
from allauth.socialaccount.models import SocialAccount  # Модель связана с социальными аккаунтами пользователей
from allauth.account.signals import user_signed_up  # импортирует сигнал
from django.dispatch import receiver  # импортирует декоратор receiver для регистрации обработчиков сигналов


# Create your models here.
@receiver(user_signed_up)  # декоратор регистрирует функцию
def add_to_common_group(request, user, **kwargs):  # будет вызываться при срабатывании сигнала
    socialaccount = SocialAccount.objects.filter(user=user).first()  # получает объект SocialAccount, связанный с новым
    # пользователем, если регистрация была совершена через социальную сеть
    if socialaccount and socialaccount.provider == 'google':  # проверяет, была ли регистрация пользователя через Google
        common_users = Group.objects.get(name='common users')  # получает объект группы с именем "common users"
        user.groups.add(common_users)  # добавляет нового пользователя в группу
