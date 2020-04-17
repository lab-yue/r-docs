# cd manuals
# wget -r -np -nH --cut-dirs=3 -R "index.html*" -A html,svg,png,jpg --no-clobber https://cran.r-project.org/doc/manuals/r-release/

for f in base/R*.html; do
  MD="src/$(cut -c6- <<< "${f%.html}.md")"
  pandoc -s "$f" -t markdown -o $MD
  sd '\{.+?\}' '' "$MD"
  sd '\[\]' '' "$MD"
  sd ':::\n(Previous|Next)[\s\S]+?:::' '' "$MD"
  sd ':::' '' "$MD"
  sd '(\n+){3,}' '\n\n' "$MD"
done
