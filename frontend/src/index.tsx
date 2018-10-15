import * as React from 'react';
import * as ReactDOM from 'react-dom';

import 'url-search-params-polyfill';

import { App } from './components/app/index';

ReactDOM.render(<App />, document.getElementById('root'));

// Hot Module Replacement
if (module.hot) {
  module.hot.accept();
}
