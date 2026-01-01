export default {
  title: 'DataCheck',
  description: 'Lightweight data quality validation for data engineers',

  head: [
    ['link', { rel: 'icon', href: '/favicon.ico' }],
    ['meta', { name: 'theme-color', content: '#3eaf7c' }],
  ],

  themeConfig: {
    logo: '/logo.svg',

    nav: [
      { text: 'Guide', link: '/guide/getting-started' },
      { text: 'Examples', link: '/examples/quick-start' },
      { text: 'API Reference', link: '/reference/cli' },
    ],

    sidebar: {
      '/guide/': [
        {
          text: 'Introduction',
          items: [
            { text: 'Getting Started', link: '/guide/getting-started' },
            { text: 'Installation', link: '/guide/installation' },
          ]
        },
        {
          text: 'Core Concepts',
          items: [
            { text: 'Validation Rules', link: '/guide/validation-rules' },
            { text: 'Configuration', link: '/guide/configuration' },
            { text: 'Data Formats', link: '/guide/data-formats' },
          ]
        }
      ],
      '/examples/': [
        {
          text: 'Examples',
          items: [
            { text: 'Quick Start', link: '/examples/quick-start' },
            { text: 'CSV Validation', link: '/examples/csv' },
            { text: 'Database Validation', link: '/examples/database' },
            { text: 'CI/CD Integration', link: '/examples/cicd' },
          ]
        }
      ],
      '/reference/': [
        {
          text: 'Reference',
          items: [
            { text: 'CLI Commands', link: '/reference/cli' },
            { text: 'Configuration Schema', link: '/reference/config' },
            { text: 'Exit Codes', link: '/reference/exit-codes' },
          ]
        }
      ]
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/yash-chauhan-dev/datacheck' }
    ],

    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2025 DataCheck'
    },

    search: {
      provider: 'local'
    }
  }
}
