import os

files = ['c:/fn/frontend/fake-news.html', 'c:/fn/frontend/phishing.html', 'c:/fn/frontend/scam-message.html', 'c:/fn/frontend/screenshot.html', 'c:/fn/frontend/tips.html']

for f_path in files:
    with open(f_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if '<main ' in content and '</main>' in content:
        head, rest = content.split('<main ', 1)
        main_content, tail = rest.split('</main>', 1)
        
        # Replace hardcoded dark-mode text classes with dynamic theme classes
        main_content = main_content.replace('text-white', 'text-primary')
        main_content = main_content.replace('text-slate-200', 'text-primary')
        main_content = main_content.replace('text-slate-300', 'text-secondary')
        main_content = main_content.replace('text-slate-400', 'text-secondary')
        main_content = main_content.replace('text-slate-500', 'text-secondary')
        main_content = main_content.replace('bg-slate-700', 'glass-card border border-accent/20')
        main_content = main_content.replace('bg-slate-800', 'bg-black/20')
        main_content = main_content.replace('border-slate-700', 'border-accent/20')
        main_content = main_content.replace('border-slate-600', 'border-accent/20')
        
        new_content = head + '<main ' + main_content + '</main>' + tail
        
        with open(f_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
