import os
import glob
import streamlit

pkg_dir = os.path.dirname(streamlit.__file__)
static_dir = os.path.join(pkg_dir, 'static')
print('Streamlit pkg:', pkg_dir)

found = []
for f in glob.glob(os.path.join(static_dir, '**', '*.js'), recursive=True):
    try:
        with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
            c = fp.read()
            for kw in ['Material Symbols', 'material-symbols', 'Material Icons', 'keyboard_double', 'arrow_right', 'stIconMaterial']:
                if kw in c:
                    found.append((os.path.basename(f), kw))
    except Exception:
        pass

for file, kw in set(found):
    print(f"File {file} contains: {kw}")
