const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8081,
    host: 'localhost',
    open: false,
    hot: true, // Hot Module Replacement
    liveReload: true, // Live reload sur changements
    watchFiles: ['src/**/*'], // Surveiller tous les fichiers src
  },
  configureWebpack: {
    cache: {
      type: 'filesystem', // Cache sur le système de fichiers
      buildDependencies: {
        config: [__filename] // Invalider le cache si la config change
      }
    }
  },
  css: {
    loaderOptions: {
      postcss: {
        postcssOptions: {
          plugins: [
            require('tailwindcss'),
            require('autoprefixer'),
          ],
        },
      },
    },
  },
})