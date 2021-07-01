module.exports = {
  devServer: {
    proxy: 'http://192.168.10.16:5050'
  },
  chainWebpack: (config) => {
    config.module
      .rule('vue')
      .use('vue-loader')
      .tap((args) => {
        args.compilerOptions.whitespace = 'preserve'
      })
  }
}
