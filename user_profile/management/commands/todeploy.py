from django.contrib.auth.models import User
from django.core.management import BaseCommand

from user_profile.models import Profile


class Command(BaseCommand):
    help = 'Creating db to deploy'

    @staticmethod
    def create_user_with_profile(username: str,
                                 email: str,
                                 firstname: str,
                                 lastname: str,
                                 password: str,
                                 is_librarian: bool):
        user_object = User.objects.create_user(username=username, email=email, password=password, first_name=firstname,
                                               last_name=lastname)
        profile_object = Profile(user=user_object, is_librarian=is_librarian)

        user_object.save()
        profile_object.save()

    def handle(self, *args, **options):
        emails_data = ['shang@gmail.com',
                       'rhialto@outlook.com',
                       'alastair@yahoo.com',
                       'rnelson@live.com',
                       'dgriffith@hotmail.com',
                       'stakasa@msn.com',
                       'papathan@yahoo.com',
                       'bflong@hotmail.com',
                       'mglee@yahoo.ca',
                       'mcast@gmail.com',
                       'rfisher@msn.com',
                       'dmbkiwi@mac.com']
        names_data = ['Felicia Medrano',
                    'Pixie Partridge',
                    'Leslie Benson',
                    'Cairon Roy',
                    'Mariana Woodley',
                    'Harriet Gonzales',
                    'Doris Boyd',
                    'Kajol Merrill',
                    'Sherri Cisneros',
                    'Debra Smyth']
        usernames_data = [
            'airplane',
            'instinctive',
            'stage',
            'intend',
            'bottle',
            'bustling',
            'wicked',
            'downtown',
            'aloof',
            'modern',
            'ocean',
            'coast',
        ]

        for i in range(len(names_data)):
            first_name, last_name = names_data[i].split()
            self.create_user_with_profile(username=usernames_data[i],
                                          email=emails_data[i],
                                          firstname=first_name,
                                          lastname=last_name,
                                          password='asdf123!',
                                          is_librarian=False)
