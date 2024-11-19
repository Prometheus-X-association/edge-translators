const path = require('path');
const TerserPlugin = require('terser-webpack-plugin');

module.exports = {
  entry: './src/index.js',
  
  devServer: {
    allowedHosts: "all"
  },
  
  mode: 'production',

  optimization: {
    minimize: true, // enables minification
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          compress: {
            drop_console: true, // removes console.log statements
          },
          format: {
            comments: false, // removes comments
          },
        },
        extractComments: false, // if you don't want a separate file for license comments
      }),
    ],
  },
  
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'esco-helper.js',
    library: "esco",
    libraryTarget: "umd",
    clean: true
  },
  
  module:{
    rules: [
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.(ttf|eot|woff|woff2|svg)$/i,
        type: 'asset/inline',
      },
    ],
  }
};