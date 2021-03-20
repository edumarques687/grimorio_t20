from django.contrib import admin
from .models import Spell
from .models import Enhancement


class EnhancementInline(admin.StackedInline):
    model = Enhancement
    extra = 1


class SpellAdmin(admin.ModelAdmin):
    inlines = [
        EnhancementInline,
    ]


admin.site.register(Spell, SpellAdmin)
admin.site.register(Enhancement)