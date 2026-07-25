from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Cash, Expense


# user registration
def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "register.html")

        if email and User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "register.html")

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        messages.success(request, "Account created successfully.")
        return redirect("login")

    return render(request, "register.html")


# user login
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:

            login(request, user)

            messages.success(request, "Login successful.")

            return redirect("dashboard")

        messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


# logout
@login_required(login_url="login")
def logout_view(request):

    logout(request)

    messages.success(request, "You have been logged out successfully.")

    return redirect("login")


# dashboard
@login_required(login_url="login")
def dashboard(request):

    cash_entries = Cash.objects.filter(user=request.user)

    expense_entries = Expense.objects.filter(user=request.user)

    total_cash = sum(cash.amount for cash in cash_entries)

    total_expense = sum(expense.amount for expense in expense_entries)

    balance = total_cash - total_expense

    entries = []

    # Income
    for cash in cash_entries:

        entries.append(
            {
                "type": "income",
                "description": cash.source
                + (" - " + cash.description if cash.description else ""),
                "amount": cash.amount,
                "created_at": cash.created_at,
            }
        )

    # Expense
    for expense in expense_entries:

        entries.append(
            {
                "type": "expense",
                "description": expense.description,
                "amount": expense.amount,
                "created_at": expense.created_at,
            }
        )

    entries.sort(
        key=lambda x: x["created_at"],
        reverse=True,
    )

    context = {
        "total_cash": total_cash,
        "total_expense": total_expense,
        "balance": balance,
        "entries": entries,
    }

    return render(
        request,
        "dashboard.html",
        context,
    )


# profile
@login_required(login_url="login")
def profile(request):

    if request.method == "POST":

        form_type = request.POST.get("form_type")

        # password
        if form_type == "profile":

            username = request.POST.get("username")
            email = request.POST.get("email")

            if (
                User.objects.exclude(id=request.user.id)
                .filter(username=username)
                .exists()
            ):

                messages.error(request, "Username already exists.")

                return redirect("profile")

            if (
                email
                and User.objects.exclude(id=request.user.id)
                .filter(email=email)
                .exists()
            ):

                messages.error(request, "Email already exists.")

                return redirect("profile")

            request.user.username = username
            request.user.email = email

            request.user.save()

            messages.success(request, "Profile updated successfully.")

            return redirect("profile")

        # password
        elif form_type == "password":

            current_password = request.POST.get("current_password")

            new_password = request.POST.get("new_password")

            confirm_password = request.POST.get("confirm_password")

            if not request.user.check_password(current_password):

                messages.error(request, "Current password is incorrect.")

                return redirect("profile")

            if new_password != confirm_password:

                messages.error(request, "New passwords do not match.")

                return redirect("profile")

            request.user.set_password(new_password)

            request.user.save()

            update_session_auth_hash(
                request,
                request.user,
            )

            messages.success(request, "Password changed successfully.")

            return redirect("profile")

        elif form_type == "delete":

            user = request.user

            logout(request)

            user.delete()

            messages.success(request, "Account deleted successfully.")

            return redirect("register")

    return render(
        request,
        "profile.html",
    )


# user profile
@login_required(login_url="login")
def profile(request):

    if request.method == "POST":

        form_type = request.POST.get("form_type")

        if form_type == "profile":

            username = request.POST.get("username")
            email = request.POST.get("email")

            if (
                User.objects.exclude(id=request.user.id)
                .filter(username=username)
                .exists()
            ):

                messages.error(request, "Username already exists.")
                return redirect("profile")

            if (
                email
                and User.objects.exclude(id=request.user.id)
                .filter(email=email)
                .exists()
            ):

                messages.error(request, "Email already exists.")
                return redirect("profile")

            request.user.username = username
            request.user.email = email
            request.user.save()

            messages.success(request, "Profile updated successfully.")
            return redirect("profile")

        elif form_type == "password":

            current_password = request.POST.get("current_password")
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            if not request.user.check_password(current_password):

                messages.error(request, "Current password is incorrect.")
                return redirect("profile")

            if new_password != confirm_password:

                messages.error(request, "New passwords do not match.")
                return redirect("profile")

            request.user.set_password(new_password)
            request.user.save()

            # Keep the user logged in
            update_session_auth_hash(request, request.user)

            messages.success(request, "Password changed successfully.")
            return redirect("profile")

        # Delete Account
        elif form_type == "delete":

            request.user.delete()

            messages.success(request, "Your account has been deleted successfully.")
            return redirect("register")

    return render(request, "profile.html")


# Add Cash
@login_required(login_url="login")
def add_cash(request):

    if request.method == "POST":

        source = request.POST.get("source")
        amount = request.POST.get("amount")
        description = request.POST.get("description")

        Cash.objects.create(
            user=request.user, source=source, amount=amount, description=description
        )

        messages.success(request, "Cash added successfully.")
        return redirect("dashboard")

    return render(request, "ManageMoney/add_money.html")


# Add Expense
@login_required(login_url="login")
def add_expense(request):

    if request.method == "POST":

        description = request.POST.get("description")
        amount = request.POST.get("amount")

        Expense.objects.create(
            user=request.user, description=description, amount=amount
        )

        messages.success(request, "Expense added successfully.")
        return redirect("dashboard")

    return render(request, "ManageMoney/add_expense.html")


# Transactions
@login_required(login_url="login")
def transactions(request):

    cash_entries = Cash.objects.filter(user=request.user)
    expense_entries = Expense.objects.filter(user=request.user)

    items = []

    # Income
    for cash in cash_entries:
        items.append(
            {
                "type": "income",
                "description": cash.source
                + (" - " + cash.description if cash.description else ""),
                "amount": cash.amount,
                "created_at": cash.created_at,
            }
        )

    # Expense
    for expense in expense_entries:
        items.append(
            {
                "type": "expense",
                "description": expense.description,
                "amount": expense.amount,
                "created_at": expense.created_at,
            }
        )

    # Latest first
    items.sort(key=lambda x: x["created_at"], reverse=True)

    context = {"items": items}

    return render(request, "ManageMoney/transactions.html", context)
