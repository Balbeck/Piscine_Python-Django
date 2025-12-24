from django.shortcuts import render, redirect
from django.conf import settings
from datetime import datetime
from .forms import LogForm
import os

# Create your views here.

def form_view(request):
    form = LogForm()
    
    if request.method == 'POST':
        form = LogForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            log_file = settings.LOG_FILE_PATH
            log_dir = os.path.dirname(log_file)
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f'[{timestamp}] {text}\n')
            
            return redirect('ex02:form')
    
    history = []
    log_file = settings.LOG_FILE_PATH
    
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line:
                    if line.startswith('[') and ']' in line:
                        timestamp_end = line.index(']')
                        timestamp = line[1:timestamp_end]
                        text = line[timestamp_end + 2:]  # +2 pour sauter '] '
                        history.append({
                            'timestamp': timestamp,
                            'text': text
                        })
    
    history.reverse() # + recent first
    
    context = {
        'form': form,
        'history': history
    }
    
    return render(request, 'form.html', context)
