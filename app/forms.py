from django import forms
from django.forms import ModelForm, inlineformset_factory
from app.utils import generate_bootstrap_widgets_for_all_fields

from . import (
    models
)

class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # field.widget.attrs['class'] = 'form-control'
            if field_name == 'phone' or field_name == 'telefone':
                field.widget.attrs['class'] = 'form-control telefone phone'
            if field_name == 'cep' or field_name == 'postalcode':
                field.widget.attrs['class'] = 'form-control cep'


class AudioForm(BaseForm, ModelForm):
    class Meta:
        model = models.Audio
        fields = ("id", "user", "filename", "cloudinary_url")
        widgets = generate_bootstrap_widgets_for_all_fields(models.Audio)

    def __init__(self, *args, **kwargs):
        super(AudioForm, self).__init__(*args, **kwargs)


class AudioFormToInline(BaseForm, ModelForm):
    class Meta:
        model = models.Audio
        fields = ("id", "user", "filename")
        widgets = generate_bootstrap_widgets_for_all_fields(models.Audio)

    def __init__(self, *args, **kwargs):
        super(AudioFormToInline, self).__init__(*args, **kwargs)


AudioUserFormSet = inlineformset_factory(models.User, models.Audio, form=AudioFormToInline, extra=1)


class ProcessForm(BaseForm, ModelForm):
    class Meta:
        model = models.Process
        fields = ("id", "user", "audio", "process_id", "status", "result")
        widgets = generate_bootstrap_widgets_for_all_fields(models.Process)

    def __init__(self, *args, **kwargs):
        super(ProcessForm, self).__init__(*args, **kwargs)


class ProcessFormToInline(BaseForm, ModelForm):
    class Meta:
        model = models.Process
        fields = ("id", "user", "audio", "status")
        widgets = generate_bootstrap_widgets_for_all_fields(models.Process)

    def __init__(self, *args, **kwargs):
        super(ProcessFormToInline, self).__init__(*args, **kwargs)


ProcessUserFormSet = inlineformset_factory(models.User, models.Process, form=ProcessFormToInline, extra=1)

ProcessAudioFormSet = inlineformset_factory(models.Audio, models.Process, form=ProcessFormToInline, extra=1)
