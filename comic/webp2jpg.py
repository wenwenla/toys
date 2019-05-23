import os
from PIL import Image

path = input('Input Path: ')
for (root, path, file) in os.walk(path):
    for f in file:
        sp = f.split('.')
        if len(sp) == 1:
            os.remove(os.path.join(root, f))
        if sp[-1] == 'webp':
            real_path = os.path.join(root, f)
            print('Processing ' + real_path)
            pic = Image.open(real_path)
            pic.save(os.path.join(root, sp[0] + '.jpg'), 'JPEG')