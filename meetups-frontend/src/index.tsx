import * as React from 'react';
import * as ReactDOM from 'react-dom';

import { App } from './components/app/index';

ReactDOM.render(<App />, document.getElementById('root'));

// Hot Module Replacement
if (module.hot) {
  module.hot.accept();
}
