from django.contrib import admin

from address.models import Address, UserAddress


class AddressAdmin(admin.ModelAdmin):
    list_display = ('country', 'state', 'city', 'zip_code', 'address_one', 'created_at', 'updated_at')
    list_filter = ('country', 'state', 'city', 'zip_code')
    search_fields = ('country', 'zip_code', 'address_one')
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Address, AddressAdmin)


class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'user', 'address', 'additional_address_data', 'created_at', 'updated_at')
    search_fields = ('user', 'address')
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(UserAddress, UserAddressAdmin)
