from django import forms

from .models import SelectedOption


class SelectOptionForm(forms.ModelForm):
    choice = forms.ChoiceField(
        choices=[
            ("yes", "Yes"),
            ("tentative", "Tentative"),
            ("no", "No"),
        ],
        initial="no",
    )
    timestamp = forms.DateTimeField(disabled=True, required=False)

    class Meta:
        model = SelectedOption
        fields = ["option", "choice", "timestamp"]
