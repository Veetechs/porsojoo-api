from django.urls import path, include
from rest_framework.routers import DefaultRouter

from categories import views

router = DefaultRouter()

router.register('questions', views.QuestionViewSet),
router.register('categories', views.CategoryViewSet),
router.register('categorieone', views.GetByCategoryOne),
router.register('categorietwo', views.GetByCategoryTwo),


app_name = 'main'

urlpatterns = [
    path('', include(router.urls)),
    path('image-upload/', views.AddImage.as_view()),
    path('add-answer/', views.QuestionAddAnswerViewSet.as_view()),
    path('like/', views.Like.as_view()),
    path('add-answer/', views.QuestionAddAnswerViewSet.as_view()),


]