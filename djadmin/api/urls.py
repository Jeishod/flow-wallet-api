from django.urls import path

from djadmin.api.views import AccountView, AccountExtendedView


urlpatterns = [
    path('accounts/', AccountView.as_view()),
    path("accounts/<str:address>/", AccountExtendedView.as_view()),
]
