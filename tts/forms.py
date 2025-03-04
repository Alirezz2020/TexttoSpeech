from django import forms

class TextToSpeechForm(forms.Form):
    file_name = forms.CharField(
        label="File Name",
        max_length=100,
        help_text="Enter a name for your MP3 file"
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter text here...'}),
        label="Text"
    )
