from rest_framework import fields, serializers
from users.models import User
from favorites.models import LikedSongsPlaylist
from favorites.serializers import LikedSongsPlaylistSerializer


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class UserSerializer(serializers.ModelSerializer):
    # favorites_playlist = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'password', 'email', 'username', 'first_name',
                  'last_name', 'date_of_birth', 'country', 'is_staff', 'is_active']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
        read_only_fields = ['id']

    # def get_favorites_playlist(self, obj):
    #     favorites_playlist = LikedSongsPlaylist.objects.get(user_id=obj.id)
    #     return LikedSongsPlaylistSerializer(favorites_playlist, context=self.context).data

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data['date_of_birth'],
            country=validated_data['country'],
            is_staff=validated_data['is_staff']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
