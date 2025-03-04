from django.views.generic import FormView
from .forms import TextToSpeechForm
from .models import ConversionHistory

from gtts import gTTS
from io import BytesIO
import base64
import uuid  # For generating unique suffixes

from django.core.files.base import ContentFile

class HomeView(FormView):
    template_name = 'tts/home.html'
    form_class = TextToSpeechForm

    def form_valid(self, form):
        text = form.cleaned_data['text']
        file_name = form.cleaned_data['file_name']
        # Ensure the file name ends with .mp3.
        if not file_name.lower().endswith('.mp3'):
            file_name = f"{file_name}.mp3"
        # Ensure the file name is unique.
        base, ext = file_name.rsplit('.', 1)
        while ConversionHistory.objects.filter(file_name=file_name).exists():
            file_name = f"{base}_{uuid.uuid4().hex[:8]}.{ext}"

        # Create the TTS audio using gTTS.
        tts = gTTS(text, lang='en')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_data = fp.read()
        # Encode the audio file to base64 so we can embed it directly in HTML.
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')

        # Save the conversion to history.
        history = ConversionHistory(text=text, file_name=file_name)
        history.audio_file.save(file_name, ContentFile(audio_data))
        history.save()

        # Retrieve all previous conversions (newest first).
        history_list = ConversionHistory.objects.all().order_by('-conversion_date')
        context = self.get_context_data(form=form, audio=audio_base64, history=history_list)
        return self.render_to_response(context)
