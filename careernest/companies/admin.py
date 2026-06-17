from django.contrib import admin
from .models import Company


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('company_name',)


admin.site.register(Company, CompanyAdmin)
