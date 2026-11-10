from pathlib import Path
import shutil
p=Path(__file__).resolve().parents[1]
for folder in ['public','dist']:
 target=p/folder;target.mkdir(exist_ok=True)
 for pattern in ['*.html','*.css','site*.js','checkout.js','delivery.js']:
  for f in p.glob(pattern):shutil.copy2(f,target/f.name)
 shutil.copytree(p/'assets',target/'assets',dirs_exist_ok=True)
for filename,script in [('checkout.html','checkout.js'),('entrega.html','delivery.js')]:
 f=p/'dist'/filename;f.write_text(f.read_text().replace(f'<script src="{script}">',f'<script>window.SITE_PREVIEW=true;</script><script src="{script}">'))
assert not list((p/'public').rglob('*.pdf'))
assert not list((p/'dist').rglob('*.pdf'))
