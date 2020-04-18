# cd manuals
# wget -r -np -nH --cut-dirs=3 -R "index.html*" -A html,svg,png,jpg --no-clobber https://cran.r-project.org/doc/manuals/r-release/

echo "# R language" >> "pages/README.md"

for f in base/R*.html; do
  FILE="$(cut -c6- <<< "${f%.html}")"
  MD="pages/$FILE/README.md"
  mkdir "pages/$FILE"
  pandoc -s "$f" -t markdown -o "$MD"
  # sd '\{.+?\}' '' "$MD"
  sd '\[\]' '' "$MD"
  sd ':::\n(Previous|Next)[\s\S]+?:::' '' "$MD"
  sd ':::' '' "$MD"
  sd '(\n+){3,}' '\n\n' "$MD"
  echo "" >> "pages/README.md"
  echo "[$FILE](/$FILE)" >> "pages/README.md"
done
