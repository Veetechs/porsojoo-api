from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from categories import models

# System base Serializers
from users.serializers import UserSerializer


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ("__all__")

        def validate(self, validated_data):
            validated_data['user'] = self.context['request'].user


# Wedding Hall Serializers
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ("__all__")
        read_only_fields = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ("__all__")
        read_only_fields = ('id',)


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ("__all__")
        read_only_fields = ('id',)


class AnswerFullSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = models.Answer
        fields = ("__all__")
        read_only_fields = ('id',)


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ("__all__")
        read_only_fields = ('id',)


class QuestionFullSerializer(serializers.ModelSerializer):
    images = ImageSerializer(
        many=True,
        read_only=True,

    )
    answers = AnswerFullSerializer(many=True, read_only=True)

    class Meta:
        model = models.Question
        fields = "__all__"
        read_only_fields = ('id',)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = "__all__"
        read_only_fields = ('id',)


class AddAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    body = serializers.CharField()


class LikeSerializer(serializers.Serializer):
    answer_id = serializers.IntegerField()
