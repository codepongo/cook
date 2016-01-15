import sys
import os
print 'mv.py'
for p in os.listdir(sys.argv[1]):
    if os.path.isdir(p):
        continue
    ext = os.path.splitext(p)[1] 
    if p[:len(sys.argv[2])] == sys.argv[2]:
        old = os.path.join(sys.argv[1], p)
        new = old.replace(sys.argv[2], sys.argv[3])
        os.system('git mv %s %s' % (old, new))
        print old, '->', new
