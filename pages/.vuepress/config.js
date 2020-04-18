const sidebar = require('./sidebar.json')
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
    sidebar
  }
}