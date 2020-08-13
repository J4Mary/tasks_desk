from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, HttpResponse

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from cards import models, forms
from cards.models import Card
from cards.permissions import CreatedByAccessPermission
from cards.serializers import CardSerializer, UserSerializer
from users.models import User


class Homepage(ListView):
    model = models.Card
    template_name = 'cards/base.html'

    def get_context_data(self, **kwargs):

        context = super(Homepage, self).get_context_data(**kwargs)
        new_cards = models.Card.objects.filter(status=1)
        in_progress_cards = models.Card.objects.filter(status=2)
        in_qa_cards = models.Card.objects.filter(status=3)
        ready_cards = models.Card.objects.filter(status=4)
        done_cards = models.Card.objects.filter(status=5)
        context.update(dict(new_cards=new_cards,
                            in_progress_cards=in_progress_cards,
                            in_qa_cards=in_qa_cards,
                            ready_cards=ready_cards,
                            done_cards=done_cards))
        return context

    def post(self, request, *args, **kwargs):
        card_id = request.POST.get('card_id', '')
        card = models.Card.objects.get(pk=card_id)
        action = request.POST.get('action')
        if action == 'next':
            card.status += 1
        elif action == 'back':
            card.status -= 1
        card.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class NewCardView(CreateView):
    model = models.Card
    form_class = forms.CardForm
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.status = 1
        self.object.created_by = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            form.fields['assigned_to'].queryset = User.objects.filter(id=self.request.user.id)
        return form


class CardEdit(UpdateView):
    model = models.Card
    form_class = forms.CardForm
    success_url = reverse_lazy('homepage')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            form.fields['assigned_to'].queryset = User.objects.filter(id=self.request.user.id)
        return form


class CardDelete(DeleteView):
    model = models.Card
    form_class = forms.CardForm
    success_url = reverse_lazy('homepage')


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [CreatedByAccessPermission]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        status = self.request.GET.get('status', None)
        if status:
            return Card.objects.all().filter(status=status)
        else:
            return Card.objects.all().filter()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ObtainTokenView(APIView):
    http_method_names = ['post']
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = authenticate(request,
                            email=self.request.data.get('email'),
                            password=self.request.data.get('password'))
        if user is not None:
            return Response(str(Token.objects.get(user=user)), 200)
        else:
            return HttpResponse(status=401)
