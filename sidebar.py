import os
import re
import json

sidebar = []
for _dir in os.listdir('./pages'):
    if not _dir.startswith('R-'):
        continue
    children = os.listdir(f'./pages/{_dir}')
    children.remove('README.md')
    # children = [l.replace('.md', '') for l in children]
    # sidebar.append({
    #     "title": _dir,
    #     "collapsable": False,
    #     "path": f'/{_dir}/',
    #     "sidebarDepth": 3,
    #     "children": [f'/{_dir}/' + l for l in sorted(children, key=lambda k: int(k.split('-')[0]))]
    # })
    for c in children:
        f = []
        with open(f'./pages/{_dir}/{c}', 'r') as r:
            f = r.readlines()
            f[0] = '# ' + f[0]

        with open(f'./pages/{_dir}/{c}', 'w') as r:
            r.writelines(f)


# with open('pages/.vuepress/sidebar.json', 'w') as f:
#     json.dump(sidebar, f)
