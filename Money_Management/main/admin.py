from django.contrib import admin
from .models import Cash, Expense


@admin.register(Cash)
class CashAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "source",
        "amount",
        "description",
        "created_at",
    )

    search_fields = (
        "user__username",
        "source",
        "description",
    )

    list_filter = (
        "user",
        "created_at",
    )

    ordering = ("-created_at",)

    date_hierarchy = "created_at"

    list_per_page = 20


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "description",
        "amount",
        "created_at",
    )

    search_fields = (
        "user__username",
        "description",
    )

    list_filter = (
        "user",
        "created_at",
    )

    ordering = ("-created_at",)

    date_hierarchy = "created_at"

    list_per_page = 20
