from django import forms

from .models import SelectedOption


class SelectOptionForm(forms.ModelForm):
    choice = forms.ChoiceField(
        choices=[
            ("yes", "Yes"),
            ("tentative", "Tentative"),
            ("no", "No"),
        ],
        required=False,
    )

    class Meta:
        model = SelectedOption
        fields = ["option", "choice"]
