import factory
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda next_number: f"magic_user_{next_number}")
    password = make_password("notvalid")

    class Meta:
        model = User
