from django.test import TestCase
from .models import Squad, SquadType, User, Volunter, VolunterType


class UserCreation(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user("test@test.com", "+38000000000", "test123123")
        self.assertNotEqual(user, None)

    def test_squad_creation(self):
        user = User.objects.create_user("test@test.com", "+38000000000", "test123123")
        self.assertNotEqual(user, None)

        squad_type = SquadType.objects.create(name="test_type")
        self.assertNotEqual(squad_type, None)
        squad = Squad.objects.create(user=user, squad_type=squad_type)
        self.assertNotEqual(squad, None)

    def test_squad_active_status(self):
        user = User.objects.create_user("test@test.com", "+38000000000", "test123123")
        self.assertNotEqual(user, None)

        squad_type = SquadType.objects.create(name="test_type")
        self.assertNotEqual(squad_type, None)
        squad = Squad.objects.create(user=user, squad_type=squad_type)
        self.assertNotEqual(squad, None)
        self.assertEqual(user.is_active, False)

    def test_volunter_creation(self):
        user = User.objects.create_user("test@test.com", "+38000000000", "test123123")
        self.assertNotEqual(user, None)
        volunter_type = VolunterType.objects.create(name="test_type")
        self.assertNotEqual(volunter_type, None)
        volunter = Volunter.objects.create(user=user, volunter_type=volunter_type)
        self.assertNotEqual(volunter, None)

    def test_superuser(self):
        user = User.objects.create_superuser(
            "test@test.com", "+380984252740", "test123123"
        )
        self.assertNotEqual(user, None)

    def test_superuser_status(self):
        user = User.objects.create_superuser(
            "test@test.com", "+380984252740", "test123123"
        )
        self.assertNotEqual(user, None)

        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_superuser, True)
        self.assertEqual(user.is_staff, True)
