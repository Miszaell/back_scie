from rest_framework import serializers

from apps.users.models import User

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email', 'name', 'last_name')

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email', 'password','name','last_name', 'date_of_birth', 'address', 'phone', 'gender', 'r_object')
        
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
    def create(self,validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
        
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'username': instance.username,
            'email': instance.email,
            'date_of_birth': instance.date_of_birth,
            'address': instance.address,
            'phone': instance.phone,
            'gender': instance.gender,
            'r_object': instance.r_object,
            # 'image': instance.image.url if instance.image != '' else '',
        }

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'last_name')

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=128, min_length=6, write_only=True)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password':'Debe ingresar ambas contraseñas iguales'}
            )
        return data

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','name','last_name', 'r_object')
        # fields = "__all__"
    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'name': instance['name'],
            'last_name': instance['last_name'] if instance['last_name'] != '' else '',
            'username': instance['username'],
            'email': instance['email'],
            'r_object': instance['r_object'],
            
        }