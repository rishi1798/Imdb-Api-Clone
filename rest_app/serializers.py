from .models import WatchList,StreamPlatform,Review
from rest_framework import serializers

class ReviewSerializer(serializers.ModelSerializer):
    review_user=serializers.StringRelatedField()
    class Meta:
        model=Review
        # fields="__all__"
        exclude=['watchlist']



class WatchListSerializer(serializers.ModelSerializer):
    
    # url=serializers.HyperlinkedIdentityField(view_name="watchlist-detail",lookup_field='pk')
    reviews=ReviewSerializer(many=True)
    # platform = serializers.HyperlinkedIdentityField(
    #     view_name="streamplatform-details",
    #     lookup_field='pk'
    # )
    class Meta:
        model=WatchList
        # exclude=['platform']
        fields="__all__"
        

class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    watchlist=WatchListSerializer(many=True)
    url=serializers.HyperlinkedIdentityField(view_name="streamplatform-details",lookup_field='pk')
    class Meta:
        model=StreamPlatform
        fields='__all__'
        






















    # def validate_name(self,value):
    #     # print(self)
    #     print(value)
    #     if len(value)<2:
    #         raise serializers.ValidationError("Name is too short!!!")
    #     else:
    #         return value

    # def get_len_name(self,object):
    #     length=len(object.name)
    #     return length

    # id=serializers.IntegerField(read_only=True)
    # name=serializers.CharField()
    # actor=serializers.CharField(max_length=30)

    # def create(self,validated_data):
    #     return Movie.objects.create(**validated_data)
    
    # def update(self,instance,validated_data):
    #     instance.name=validated_data.get('name',instance.name)
    #     instance.actor=validated_data.get('actor',instance.actor)

    #     instance.save()
    #     return instance
    
    
        
