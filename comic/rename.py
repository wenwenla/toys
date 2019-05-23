import os
import shutil

fp = input('Input path:')

if not os.path.exists(os.path.join(fp, 'out')):
    os.mkdir(os.path.join(fp, 'out'))

for (root, path, file) in os.walk(fp):
    if root.split('\\')[-1] == 'out':
        continue
    for f in file:
        sp = f.split('.')
        if sp[-1] == 'jpg':
            src = os.path.join(root, f)
            dest = os.path.join(fp, 'out', '{}_{:03d}.jpg'.format(root.split('\\')[-1], int(sp[0])))
            print('copy {} to {}'.format(src, dest))
            shutil.copyfile(src, dest)
