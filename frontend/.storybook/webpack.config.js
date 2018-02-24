const path = require('path');

const SRC_PATH = path.join(__dirname, '../src');

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
    enforceExtension: false
  }
};
