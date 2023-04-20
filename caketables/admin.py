from django.contrib import admin
from .models import UserTable, Visitor


# 케이크 생성
@admin.register(UserTable)
class UsertableAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Birthday Table",
            {
                "fields": (
                    "owner",
                    "nickname",
                    "tablecolor",
                ),
                "classes": ("wide",),
            },
        ),
    )

    list_display = ("pk", "owner", "nickname","total_visitor")
    list_display_links = ("pk", "owner", "nickname","total_visitor")

    list_filter = ("owner", "nickname")

    search_fields = ("owner", "nickname")


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Decoration",
            {
                "fields": (
                    "owner",
                    "pickcake",
                    "letter",
                    "visitor_name",
                    "visitor_password",
                )
            },
        ),
    )

    list_display = ("pk", "owner","pickcake", "visitor_name")
    list_display_links = ("pk", "owner", "pickcake", "visitor_name")

    list_filter = ("owner", "pickcake", "visitor_name")

    search_fields = ("pk", "owner", "visitor_name")
