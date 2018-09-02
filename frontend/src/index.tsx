import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { Router, RouteComponentProps } from '@reach/router';
import { ApolloProvider } from 'react-apollo';

import { Admin } from './pages/admin';

import { client } from './client';

import './index.css';

const Home = (props: RouteComponentProps) => <div>Home</div>;
const Dash = (props: RouteComponentProps) => <div>Dash</div>;

const App = () => (
  <ApolloProvider client={client}>
    <Router>
      <Home path="/" />
      <Dash path="dashboard" />
      <Admin path="/admin/*" />
    </Router>
  </ApolloProvider>
);

ReactDOM.render(<App />, document.getElementById('root'));

// Hot Module Replacement
if (module.hot) {
  module.hot.accept();
}
