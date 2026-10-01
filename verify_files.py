"""Check all data against the delivery manifest. Standard library only."""
from pathlib import Path
import hashlib,json,sys

root=Path(__file__).resolve().parent
manifest=json.loads((root/'data-manifest.json').read_text(encoding='utf-8'))
failed=[]
for entry in manifest['files']:
    path=(root/entry['path']).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        failed.append(entry['path']);continue
    h=hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda:source.read(1024*1024),b''):h.update(block)
    if path.stat().st_size!=entry['bytes'] or h.hexdigest()!=entry['sha256']:
        failed.append(entry['path'])
print(json.dumps({'files':len(manifest['files']),'failed_count':len(failed)},ensure_ascii=False))
sys.exit(1 if failed else 0)
