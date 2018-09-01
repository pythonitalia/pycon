import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { Router, Link, RouteComponentProps } from '@reach/router';

import './index.css';

const Home = (props: RouteComponentProps) => <div>Home</div>;
const Dash = (props: RouteComponentProps) => <div>Dash</div>;

const App = () => (
  <Router>
    <Home path="/" />
    <Dash path="dashboard" />
  </Router>
);

ReactDOM.render(<App />, document.getElementById('root'));

// Hot Module Replacement
if (module.hot) {
  module.hot.accept();
}
