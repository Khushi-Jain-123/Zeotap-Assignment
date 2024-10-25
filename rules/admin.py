# rules/admin.py

from django.contrib import admin
from .models import Node, Rule
import json

class NodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'value')  # Display ID, type, and value in the admin list view

admin.site.register(Node, NodeAdmin)

@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('rule_string', 'created_at')
    readonly_fields = ('ast',)

    def ast_display(self, obj):
        return json.dumps(obj.ast, indent=2)  # Format the JSON for display

    ast_display.short_description = 'AST'
