from django.urls import path
from . import views

urlpatterns = [
    path("", views.register, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    # Add Money
    path("add-cash/", views.add_cash, name="add_cash"),
    # Add Expense
    path("add-expense/", views.add_expense, name="add_expense"),
    # transitions
    path("transactions/", views.transactions, name="transactions"),
]
