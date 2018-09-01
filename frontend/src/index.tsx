import * as React from 'react';
import * as ReactDOM from 'react-dom';

import './index.css';

import { Title } from './components/title';

const App = () => (
  <div>
    <Title>Hello world!</Title>
  </div>
);

ReactDOM.render(<App />, document.getElementById('root'));

// Hot Module Replacement
if (module.hot) {
  module.hot.accept();
}
