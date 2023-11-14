from django import forms
from taskify.models import Task, TaskStatus


class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("name", "description", "status", "dynamic_fields")


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("name", "description", "dynamic_fields")


class SearchTaskForm(forms.Form):
    id = forms.IntegerField(required=False)
    name = forms.CharField(required=False)
    status = forms.ChoiceField(choices=[(len(TaskStatus), "Not Important")] + TaskStatus.choices, required=False)
    dynamic_fields = forms.CharField(required=False, widget=forms.Textarea())
