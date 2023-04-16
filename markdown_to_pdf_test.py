import markdown
import weasyprint
from pathlib import Path

test_file = Path('test.md')
output_pdf = Path('test.pdf')

with open(test_file, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('{title}', 'TEST TITLE').replace('{year}', str(2023)).replace('{artist}', 'ARTIST NAME')

html = markdown.markdown(text)

css = weasyprint.CSS(string='body { font-family: calibri }')
weasyprint.HTML(string=html).write_pdf(output_pdf, stylesheets=[css])