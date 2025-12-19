/**
 * Docusaurus plugin for injecting translation buttons at the start of each chapter
 */

const path = require('path');

/** @type {import('@docusaurus/types').PluginModule} */
module.exports = function translationPlugin(context, options) {
  return {
    name: 'translation-plugin',

    // Extend the default Docusaurus lifecycle methods
    async contentLoaded({ content, actions }) {
      // This plugin doesn't load additional content, but we can use this hook
      // to modify existing content if needed
    },

    // Configure Webpack to handle our translation components
    configureWebpack(config, isServer, utils) {
      return {
        resolve: {
          alias: {
            '@site/src/components/TranslationButton': path.resolve(
              __dirname,
              '../components/TranslationButton.jsx'
            ),
            '@site/src/hooks/useLanguageSwitch': path.resolve(
              __dirname,
              '../hooks/useLanguageSwitch.js'
            ),
            '@site/src/utils/scrollUtils': path.resolve(
              __dirname,
              '../utils/scrollUtils.js'
            ),
            '@site/src/utils/chapterUtils': path.resolve(
              __dirname,
              '../utils/chapterUtils.js'
            ),
          },
        },
      };
    },

    // Add CSS for RTL support
    getThemePath() {
      return path.resolve(__dirname, '../theme');
    },

    // Inject translation styles
    injectHtmlTags() {
      return {
        headTags: [
          {
            tagName: 'link',
            attributes: {
              rel: 'stylesheet',
              href: '/css/rtl-styles.css',
            },
            innerHTML: '',
          },
          {
            tagName: 'link',
            attributes: {
              rel: 'stylesheet',
              href: '/css/button-styles.css',
            },
            innerHTML: '',
          },
        ],
      };
    },
  };
};

// Export plugin configuration type for TypeScript
module.exports.validateOptions = ({ options }) => {
  return options;
};