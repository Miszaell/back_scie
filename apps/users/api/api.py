from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import viewsets
from rest_framework.parsers import JSONParser, MultiPartParser
from apps.users.models import User
from apps.users.api.serializers import (
    CustomUserSerializer, UserListSerializer, UpdateUserSerializer,
    PasswordSerializer, UserSerializer
)


class UserViewSet(viewsets.GenericViewSet):
    model = User
    serializer_class = CustomUserSerializer
    list_serializer_class = UserListSerializer
    parser_classes = (JSONParser, MultiPartParser)
    queryset = None
    permission_classes = [DjangoModelPermissions]

    def get_object(self, pk):
        obj = get_object_or_404(self.model, pk=pk)
        self.check_object_permissions(self.model, obj)
        return obj

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects\
                .filter(is_active=True)
        return self.queryset

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object(pk)
        password_serializer = PasswordSerializer(data=request.data)
        if password_serializer.is_valid():
            user.set_password(password_serializer.validated_data['password'])
            user.save()
            return Response({
                'message': 'Password updated successfully'
            })
        return Response({
            'message': 'There are errors in the information received',
            'errors': password_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        print(request.user)
        users = self.get_queryset()
        users_serializer = self.list_serializer_class(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message': 'Successfully registered user.'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'There are errors in the registry',
            'errors': user_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = self.serializer_class(user)
        return Response(user_serializer.data)

    def update(self, request, pk=None):
        user = self.get_object(pk)
        if user:
            # if request.data['image']:
            #     data = validate_files(request.data, 'image', True)
            #     user_serializer = UpdateUserSerializer(user, data=data)
            # else:
            user_serializer = UpdateUserSerializer(user, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response({
                    'message': 'Successfully updated user'
                }, status=status.HTTP_200_OK)
            return Response({
                'message': 'There are errors in the update',
                'errors': user_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    def patch(self, request, pk):
        user = self.get_object(pk)
        if user:
            user_serializer = UserSerializer(user, data=request.data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response({
                    'message': 'Successfully partial updated user'
                }, status=status.HTTP_200_OK)
            return Response({
                'message': 'There are errors in the partial update',
                'errors': user_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        user_destroy = self.model.objects.filter(id=pk).update(is_active=False)
        if user_destroy == 1:
            return Response({
                'message': 'Successfully deleted user'
            })
        return Response({
            'message': 'The user you want to delete does not exist'
        }, status=status.HTTP_404_NOT_FOUND)