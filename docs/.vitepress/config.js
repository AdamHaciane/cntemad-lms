import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'CNTEMAD LMS',
  description: 'Documentation de la plateforme LMS du Centre National de Télé-Enseignement de Madagascar',

  head: [
    ['link', { rel: 'icon', href: '/favicon.ico' }],
    ['meta', { name: 'theme-color', content: '#1e40af' }],
    ['meta', { name: 'og:type', content: 'website' }],
    ['meta', { name: 'og:site_name', content: 'CNTEMAD LMS Docs' }],
  ],

  // Base URL pour GitHub Pages
  base: '/cntemad-lms/',

  // Langues
  locales: {
    root: {
      label: 'Français',
      lang: 'fr',
      link: '/fr/'
    },
    mg: {
      label: 'Malagasy',
      lang: 'mg',
      link: '/mg/'
    }
  },

  themeConfig: {
    logo: '/logo.svg',
    siteTitle: 'CNTEMAD LMS',

    // Navigation principale
    nav: [
      { text: 'Accueil', link: '/' },
      { text: 'Étudiant', link: '/fr/etudiant/inscription' },
      { text: 'Enseignant', link: '/fr/enseignant/creer-cours' },
      { text: 'Admin', link: '/fr/admin/dashboard' },
      { text: 'Technique', link: '/fr/technique/api' }
    ],

    // Sidebar par section
    sidebar: {
      '/fr/etudiant/': [
        {
          text: 'Guide Étudiant',
          items: [
            { text: 'Inscription', link: '/fr/etudiant/inscription' },
            { text: 'Paiement', link: '/fr/etudiant/paiement' },
            { text: 'Suivre un cours', link: '/fr/etudiant/cours' },
            { text: 'FAQ', link: '/fr/etudiant/faq' }
          ]
        }
      ],
      '/fr/enseignant/': [
        {
          text: 'Guide Enseignant',
          items: [
            { text: 'Créer un cours', link: '/fr/enseignant/creer-cours' },
            { text: 'Évaluations', link: '/fr/enseignant/evaluations' }
          ]
        }
      ],
      '/fr/admin/': [
        {
          text: 'Guide Administrateur',
          items: [
            { text: 'Dashboard', link: '/fr/admin/dashboard' },
            { text: 'Rapports', link: '/fr/admin/rapports' }
          ]
        }
      ],
      '/fr/technique/': [
        {
          text: 'Documentation Technique',
          items: [
            { text: 'API Reference', link: '/fr/technique/api' },
            { text: 'Doctypes', link: '/fr/technique/doctypes' },
            { text: 'Contribuer', link: '/fr/technique/contributing' }
          ]
        }
      ],
      '/mg/etudiant/': [
        {
          text: 'Torolàlana ho an\'ny Mpianatra',
          items: [
            { text: 'Fisoratana anarana', link: '/mg/etudiant/inscription' },
            { text: 'Fandoavana', link: '/mg/etudiant/paiement' },
            { text: 'Fanarahan-taratra', link: '/mg/etudiant/cours' },
            { text: 'FAQ', link: '/mg/etudiant/faq' }
          ]
        }
      ],
      '/mg/enseignant/': [
        {
          text: 'Torolàlana ho an\'ny Mpampianatra',
          items: [
            { text: 'Mamorona lesona', link: '/mg/enseignant/creer-cours' },
            { text: 'Fanombanana', link: '/mg/enseignant/evaluations' }
          ]
        }
      ],
      '/mg/admin/': [
        {
          text: 'Torolàlana ho an\'ny Mpitantana',
          items: [
            { text: 'Dashboard', link: '/mg/admin/dashboard' },
            { text: 'Tatitra', link: '/mg/admin/rapports' }
          ]
        }
      ],
      '/mg/technique/': [
        {
          text: 'Tahirin-kevitra Teknika',
          items: [
            { text: 'API Reference', link: '/mg/technique/api' },
            { text: 'Doctypes', link: '/mg/technique/doctypes' },
            { text: 'Mandray anjara', link: '/mg/technique/contributing' }
          ]
        }
      ]
    },

    // Liens sociaux
    socialLinks: [
      { icon: 'github', link: 'https://github.com/cntemad-mg/cntemad-lms' }
    ],

    // Footer
    footer: {
      message: 'Fait avec ❤️ à Madagascar | Supporté par SAYNA',
      copyright: '© 1992-2026 CNTEMAD Madagascar'
    },

    // Recherche
    search: {
      provider: 'local',
      options: {
        locales: {
          root: {
            translations: {
              button: {
                buttonText: 'Rechercher',
                buttonAriaLabel: 'Rechercher'
              },
              modal: {
                noResultsText: 'Aucun résultat pour',
                resetButtonTitle: 'Effacer',
                footer: {
                  selectText: 'Sélectionner',
                  navigateText: 'Naviguer',
                  closeText: 'Fermer'
                }
              }
            }
          }
        }
      }
    },

    // Éditer sur GitHub
    editLink: {
      pattern: 'https://github.com/cntemad-mg/cntemad-lms/edit/main/docs/:path',
      text: 'Modifier cette page sur GitHub'
    },

    // Dernière mise à jour
    lastUpdated: {
      text: 'Dernière mise à jour',
      formatOptions: {
        dateStyle: 'short',
        timeStyle: 'short'
      }
    },

    // Navigation docs
    docFooter: {
      prev: 'Page précédente',
      next: 'Page suivante'
    },

    outline: {
      label: 'Sur cette page'
    },

    returnToTopLabel: 'Retour en haut'
  }
})
