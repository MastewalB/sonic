from rest_framework import serializers
from follow.models import Follow


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['follower', 'followee']
        read_only_fields = ['follower']
    
    def create(self, validated_data):
        follow = Follow(
            followee=validated_data['followee'] ,
            follower = self.context['follower']
        )
        follow.save()
        return follow

class FollowerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow  
        fields = ['follower']