from django.contrib import admin

from djadmin.base.models import Accounts, Jobs


@admin.register(Jobs)
class JobsAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "result",
        "transaction_id",
        "created_at",
        "updated_at",
        "deleted_at",
        "state",
        "exec_count",
        "type",
    ]
    readonly_fields = [field.name for field in Jobs._meta.fields]   # noqa


@admin.register(Accounts)
class AccountsAdmin(admin.ModelAdmin):
    list_display = [
        "address",
        "type",
        "created_at",
        "updated_at",
        "deleted_at",
    ]
    readonly_fields = [field.name for field in Accounts._meta.fields]   # noqa
