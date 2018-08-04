from django import forms
from Main.models import Profile

class Update(forms.ModelForm):
	class Meta:
		model = Profile

		fields=[
			"location",
			"image",
		]