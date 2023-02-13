from django.contrib.sessions.models import Session
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from apps.users.api.serializers import UserTokenSerializer
from rest_framework.authentication import get_authorization_header
class UserToken(APIView):
    def post(self,request,*args,**kwargs):
        email = request.data['email']
        try:
            user_token = Token.objects.get(
                user = UserTokenSerializer().Meta.model.objects.filter(email = email).first()
            )
            return Response({
                'token': user_token.key
            })
        except:
            return Response({'error': 'The credentials received are incorrect.'},status = status.HTTP_401_UNAUTHORIZED)
                            
class Login(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data = request.data, context = {'request':request})
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                token,created = Token.objects.get_or_create(user = user)
                user_serializaer = UserTokenSerializer(user)
                if created:
                    return Response({
                        'token': token.key,
                        'user':user_serializaer.data
                        }, status = status.HTTP_201_CREATED)
                else:
                    all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                    if all_sessions.exists():
                        for session in all_sessions:
                            session_data = session.get_decoded()
                            if user.id == int(session_data.get('_auth_user_id')):
                                session.delete()
                    token.delete()
                    token = Token.objects.create(user = user)
                    return Response({
                        'token': token.key,
                        'user': user_serializaer.data
                    }, status=status.HTTP_201_CREATED)
            else:
                return Response({'error':'This user is disabled'}, status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Invalid username or password'}, status = status.HTTP_401_UNAUTHORIZED)

class Logout(APIView):
    def post(self, request, *args, **kwargs):
        try:
            token = get_authorization_header(request).split()
            try:
                token = token[1].decode()
            except:
                return None
            token = Token.objects.filter(key=token).first()

            if token:
                user = token.user
                all_sessions = Session.objects.filter(
                    expire_date__gte=datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                token.delete()
                return Response({'token_message': 'Deleted token.', 'session_message': 'Deleted user sessions.'},
                                status=status.HTTP_200_OK)

            return Response({'error': 'A user with these credentials was not found.'},
                            status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'No token found in request.'},
                            status=status.HTTP_409_CONFLICT)