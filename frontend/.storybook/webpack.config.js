const path = require('path');
const TsconfigPathsPlugin = require('tsconfig-paths-webpack-plugin');

const SRC_PATH = path.join(__dirname, '../src');
const TSCONFIG_PATH = path.join(__dirname, '../tsconfig.json');

module.exports = {
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        loader: 'ts-loader',
        include: [SRC_PATH]
      },
      {
        loader: 'style-loader!css-loader',
        test: /\.css$/
      }
    ]
  },

  resolve: {
    extensions: ['.ts', '.tsx', '.js', '.jsx'],
    enforceExtension: false,
    plugins: [
      new TsconfigPathsPlugin({
        configFile: TSCONFIG_PATH
      })
    ]
  }
};
