import markdown
import weasyprint
from pathlib import Path

test_file = Path('test.md')

with open(test_file, 'r', encoding='utf-8') as f:
    text = f.read()
html = markdown.markdown(text)

weasyprint.HTML(string=html).write_pdf('test.pdf')

# with open('test.html', 'w', encoding='utf-8') as f:
#     f.write(html)

