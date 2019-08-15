import os
import re

base_dir = r""

for subdir, dirs, files in os.walk(base_dir):
    # if not os.path.isdir(os.path.join(base_dir, dir)):
    #     continue

    # print(subdir)

    for dir in dirs:
        pattern = r"\s{2,}"
        replace = " "
        new_name = re.sub(pattern, replace, dir)
        if os.path.join(base_dir, dir) != os.path.join(base_dir, new_name):
            print(os.path.join(base_dir, subdir, dir))
            print(os.path.join(base_dir, subdir, new_name))
            print("=================================")

            os.rename(os.path.join(base_dir, subdir, dir), os.path.join(base_dir, new_name))
