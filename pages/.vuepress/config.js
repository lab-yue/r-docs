module.exports = {
  title: 'R language',
  description: 'introduction to R language',
  head: [
    ['link', { rel: 'icon', href: '/logo.jpg' }]
  ],
  themeConfig: {
    themeConfig: {
      displayAllHeaders: true,
      collapsable: false
    },
    nav: [
      { text: 'Github', link: 'https://github.com/rainy-me/' },
      { text: 'Twitter', link: 'https://twitter.com/nerd_yue/' },
    ],
    sidebar: [
      "/R-intro",
      "/R-lang",
      "/R-data",
      "/R-admin",
      "/R-exts",
      "/R-ints",
      "/R-FAQ"
    ]
  }
}