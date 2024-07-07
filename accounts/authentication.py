# third party
from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
   def authenticate(self, request):
       access_token = request.COOKIES.get('access_token')
       if not access_token:
           return None
       if isinstance(access_token,str):
           access_token = access_token.encode()

       validated_token = self.get_validated_token(access_token)

       return self.get_user(validated_token), validated_token