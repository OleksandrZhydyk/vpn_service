from django import forms

from sites.models import Site


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ("url", "name",)

        widgets = {
            "url": forms.TextInput(
                attrs={
                    "class": "form-control rounded border border-success p-2 mb-2",
                    "placeholder": "Url"
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control rounded border border-success p-2 mb-2",
                    "placeholder": "Site name"
                }
            ),
        }
