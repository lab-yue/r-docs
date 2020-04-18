import os
import re
import json

sidebar = []
for _dir in os.listdir('./pages'):
    if not _dir.startswith('R-'):
        continue
    # children = os.listdir(f'./pages/{_dir}')
    # children.remove('README.md')
    # children = [l.replace('.md', '') for l in children]
    # sidebar.append({
    #     "title": _dir,
    #     "collapsable": False,
    #     "path": f'/{_dir}/',
    #     "sidebarDepth": 3,
    #     "children": [f'/{_dir}/' + l for l in sorted(children, key=lambda k: int(k.split('-')[0]))]
    # })
    c = ""
    with open(f'./pages/{_dir}/README.md', 'r') as r:
        c = r.read()
    with open(f'./pages/{_dir}/README.md', 'w') as r:
        r.write(c.split("\n## 1")[0])


# with open('pages/.vuepress/sidebar.json', 'w') as f:
#     json.dump(sidebar, f)
