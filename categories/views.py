from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework import filters
from categories import custom_permissions
from rest_framework import permissions, response, generics
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from categories import custom_response, custom_exception
from categories import models
from categories import serializers
from rest_framework.parsers import FileUploadParser

from django.conf import settings

from categories.models import Question


class AddImage(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    parser_class = (FileUploadParser,)

    def post(self, request):

        if request.data["image"].size > (int(settings.MAX_UPLOAD_SIZE)):
            return JsonResponse({
                "data": custom_exception.exception(f'file bigger than {settings.MAX_UPLOAD_SIZE} mb', False)
            }, status=status.HTTP_400_BAD_REQUEST)
        file_serializer = serializers.ImageSerializer(data=request.data)
        request.data['user'] = request.user.pk
        if file_serializer.is_valid(request.data):
            file_serializer.save()
            return response.Response(
                file_serializer.data,
                status=status.HTTP_200_OK
            )

        return HttpResponse(
            file_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class BaseQuestionViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin
):
    authentication_classes = (TokenAuthentication,)
    search_fields = ['tag', 'title', 'body']
    filter_backends = (filters.SearchFilter,)

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [custom_permissions.IsAdminOrOwner]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QuestionViewSet(BaseQuestionViewSet):
    queryset = models.Question.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.QuestionFullSerializer
        if self.action == 'list':
            return serializers.QuestionFullSerializer
        return serializers.QuestionSerializer


class BaseAnswerViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QuestionAnswerViewSet(BaseAnswerViewSet):
    queryset = models.Answer.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.AnswerFullSerializer
        if self.action == 'list':
            return serializers.AnswerFullSerializer
        return serializers.AnswerFullSerializer


#
#
class QuestionAddAnswerViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        add_answer = serializers.AddAnswerSerializer(data=request.data)
        add_answer.is_valid(request.data)

        review_model = {
            "question": add_answer.data['question_id'],
            "user": request.user.pk,
            "body": add_answer.data['body'],
        }

        answer_serializer = serializers.AnswerSerializer(data=review_model)
        answer_serializer.is_valid(review_model)
        answer = serializers.AnswerSerializer.save(answer_serializer)
        answer.save()
        question = models.Question.objects.get(
            pk=add_answer.data['question_id']
        )
        question.answers.add(answer)
        return JsonResponse({
            "data": custom_response.custom_response("successfully created!",
                                                    {"review": answer_serializer.data})
        }, status=status.HTTP_200_OK)


class CategoryBaseViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin):
    authentication_classes = (TokenAuthentication,)

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryViewSet(BaseAnswerViewSet):
    queryset = models.Category.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.CategorySerializer
        if self.action == 'list':
            return serializers.CategorySerializer
        return serializers.CategorySerializer


class Like(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        like_serializer = serializers.LikeSerializer(data=request.data)
        like_serializer.is_valid(request.data)
        answer = models.Answer.objects.get(pk=request.data['answer_id'])
        if answer is None:
            return JsonResponse({
                "data": custom_exception.exception("answer not found", False)
            }, status=status.HTTP_400_BAD_REQUEST)
        answer.likes = answer.likes + 1
        answer.save()
        return JsonResponse({
            "data": custom_response.custom_response("successfully liked!", {})
        }, status=status.HTTP_200_OK)


class DisLike(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        like_serializer = serializers.LikeSerializer(data=request.data)
        like_serializer.is_valid(request.data)
        answer = models.Answer.objects.get(pk=request.data['answer_id'])
        if answer is None:
            return JsonResponse({
                "data": custom_exception.exception("answer not found", False)
            }, status=status.HTTP_400_BAD_REQUEST)
        answer.dis_likes = answer.dis_likes + 1
        answer.save()
        return JsonResponse({
            "data": custom_response.custom_response("successfully disliked!", {})
        }, status=status.HTTP_200_OK)


class GetByCategoryBase(viewsets.GenericViewSet,
                       mixins.ListModelMixin):
    permission_classes = [permissions.AllowAny]

    authentication_classes = (TokenAuthentication,)


class GetByCategoryOne(GetByCategoryBase):
    queryset = Question.objects.filter(category_id=1)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.QuestionFullSerializer
        if self.action == 'list':
            return serializers.QuestionFullSerializer
        return serializers.QuestionSerializer


class GetByCategoryTwo(GetByCategoryBase):
    queryset = Question.objects.filter(category_id=2)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.QuestionFullSerializer
        if self.action == 'list':
            return serializers.QuestionFullSerializer
        return serializers.QuestionSerializer