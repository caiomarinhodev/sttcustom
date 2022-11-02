#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.apps import apps
from django.contrib import admin

# Register your models here.

from app.models import *


def approve_selected(modeladmin, request, queryset):
    queryset.update(is_approved=True)


def desapprove_selected(modeladmin, request, queryset):
    queryset.update(is_approved=False)


approve_selected.short_description = "Aprovar itens selecionados"
desapprove_selected.short_description = "Desaprovar itens selecionados"


class ProcessInline(admin.TabularInline):
    model = Process



class AudioAdmin(admin.ModelAdmin):
    list_filter = []
    search_fields = (
        'id',
    )
    inlines = [ProcessInline]
    list_display = ("id", "user", "filename")

admin.site.register(Audio, AudioAdmin)


class ProcessAdmin(admin.ModelAdmin):
    list_filter = []
    search_fields = (
        'id',
    )
    inlines = []
    list_display = ("id", "user", "audio", "status")

admin.site.register(Process, ProcessAdmin)
