from django.contrib import admin
from .models import Car, Category,FuelType,Maker,ModelName,Province,City,CarImage,CarFeature


class CarAdmin(admin.ModelAdmin):
    list_display = ('title','agent', 'maker', 'model', 'year', 'price', 'is_featured', 'created_at')
    # search_fields = ('title', 'album__title')

    def has_add_permission(self, request, obj=None):
       
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
       
        return request.user.is_superuser

admin.site.register(Car, CarAdmin)
admin.site.register(Category) 


@admin.register(FuelType)
class FuelTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Maker)
class MakerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ModelName)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'maker')
    list_filter = ('maker',)
    search_fields = ('name', 'maker__name')

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')
    list_filter = ('state',)
    search_fields = ('name', 'state__name')

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1
    fields = ('image', 'is_main')

class CarFeatureInline(admin.TabularInline):
    model = CarFeature
    extra = 1