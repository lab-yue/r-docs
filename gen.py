import os
import re

chapter_re = re.compile(r'^(.+?) \{.+\.chapter\}$', flags=re.M)
section_re = re.compile(r'\n^### .+$', flags=re.M)
bad_link_re = re.compile(r'(\[.+)\n([a-z]+\]\()')
chapter_link_re = re.compile(r':::\n(Previous|Next)[\s\S]+?:::')

for _dir in os.listdir('./pages'):
    if not _dir.startswith('R-'):
        continue
    print(_dir)
    with open(f"pages/{_dir}/README.md", 'r') as file:
        content = file.read()

        content = chapter_link_re.sub('', content)
        content = bad_link_re.sub(r'\1 \2', content)
        content.replace(':::', '')
        chapters = chapter_re.split(content)

        file_name = ''
        file_output = []
        for i, part in enumerate(chapters[1:]):
            file_output.append(part)
            if not (i & 1):
                file_name = part.replace('#', '').strip().replace(' ', '-')
            else:
                print(f"pages/{_dir}/{file_name}.md")
                with open(f"pages/{_dir}/{file_name}.md", 'a') as chapter:
                    chapter.write("\n".join(file_output))
                file_output = []
