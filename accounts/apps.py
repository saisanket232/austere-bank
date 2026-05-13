from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from django import forms
        # Patch all form fields to use bootstrap classes
        original_init = forms.Field.__init__
        def bootstrap_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            if hasattr(self, 'widget'):
                widget = self.widget
                if isinstance(widget, (forms.TextInput, forms.EmailInput, forms.PasswordInput, forms.NumberInput, forms.DateInput, forms.URLInput, forms.TimeInput)):
                    widget.attrs.setdefault('class', 'form-control')
                elif isinstance(widget, forms.Select):
                    widget.attrs.setdefault('class', 'form-select')
                elif isinstance(widget, forms.Textarea):
                    widget.attrs.setdefault('class', 'form-control')
        forms.Field.__init__ = bootstrap_init
