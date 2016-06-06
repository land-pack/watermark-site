import os

# Get the current path
project_path = os.path.abspath('.')
# write supervisor configure file auto
with open('watermark-site.conf', "w") as f:
    f.write('[program:app]\n')
    f.write('command')
    f.write(project_path)
