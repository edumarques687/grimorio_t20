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


class EnhancementAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'cost', 'related_spell']
    list_filter = ['related_spell']
    search_fields = ['cost', 'effect', 'related_spell__name']


admin.site.register(Spell, SpellAdmin)
admin.site.register(Enhancement, EnhancementAdmin)
