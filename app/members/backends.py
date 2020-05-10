# from django.contrib.auth.backends import ModelBackend
#
# from config.settings.base import AUTH_USER_MODEL
#
# User = AUTH_USER_MODEL
#
#
# class EmailBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             user = User.objects.get(email=username)
#         except user.DoesNotExist:
#             return None
#         else:
#             if user.check_password(password):
#                 return user
#         return None
