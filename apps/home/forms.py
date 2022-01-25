

from django import forms

class TrendsRequest(forms.Form):

    keywords = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                            'placeholder':'Introduce all the keywords separated by commas'}))