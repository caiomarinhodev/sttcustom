#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, RedirectView
from django.views.generic.edit import (
    FormView
)

try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.urls import reverse_lazy, reverse

from app.forms import AudioForm


class IndexView(LoginRequiredMixin, TemplateView):
    """
    Index of Audio
    """
    login_url = '/admin/login/'
    template_name = 'dashboard.html'


class AudioView(LoginRequiredMixin, FormView):
    """
    Audio View
    """
    login_url = '/admin/login/'
    template_name = 'upload/upload_audio.html'
    form_class = AudioForm


class RecordView(LoginRequiredMixin, FormView):
    """
    Record View
    """
    login_url = '/admin/login/'
    template_name = 'upload/recorder_audio.html'
    form_class = AudioForm


class RedirectToViewProcess(LoginRequiredMixin, RedirectView):
    """
    Redirect to view process
    """
    login_url = '/admin/login/'
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        data = self.request.GET
        return reverse('PROCESS_detail', kwargs={'pk': data['pk']})
