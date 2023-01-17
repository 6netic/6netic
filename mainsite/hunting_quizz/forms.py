from django.forms import ModelForm
from . models import Hunting
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User


class add_question_form(ModelForm):
    """  """

    class Meta:
        model = Hunting
        fields = '__all__'


# class create_user_form(UserCreationForm):
#     """  """
#
#     class Meta:
#         model = User
#         fields = ['username', 'password']



