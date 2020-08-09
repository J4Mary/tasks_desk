from django.urls import include, path

from cards import views


urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),
    path('cards/new', views.NewCardView.as_view(), name='new_card'),
    path('cards/<int:pk>/edit', views.CardEdit.as_view(), name='card_edit'),
    path('card/<int:pk>/delete', views.CardDelete.as_view(), name='card_delete'),

]
