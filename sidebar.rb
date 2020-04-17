
require 'json'
# exclude = ['about-me.md','index.md'].map!{ |file| './pages/' + file}
File.open("./pages/.vuepress/sidebar.json","a+") do |f|
    f.write(
        {
            "data" => Dir["./pages/*.md"]
  #                      .select { |file| not exclude.index(file) }
                        .map!   { |file| '/' + file.split("/")[-1].split('.')[0] }
        }.to_json)
end