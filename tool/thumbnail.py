import stbi
import sys
import os
i = 0
for p in os.listdir(sys.argv[1]):
    if os.path.isdir(p):
        continue
    ext = os.path.splitext(p)[1] 
    if ext == '.jpg' or ext == '.JPG':
        old = os.path.join(sys.argv[1], p)
        new = '%s-%02d.jpg' % (sys.argv[2], i)
        print old, '->', new
        stbi.open(old).resize(480, 360).save(new)
        i += 1
