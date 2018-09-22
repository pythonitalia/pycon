import * as React from 'react';

import { Router, RouteComponentProps } from '@reach/router';
import { ApolloProvider } from 'react-apollo';

import { Admin } from '../../pages/admin';

import { client } from './client';

import './base.css';
import './typography.css';

const Home = (props: RouteComponentProps) => <div>Home</div>;
const Dash = (props: RouteComponentProps) => <div>Dash</div>;

export const App = () => (
  <ApolloProvider client={client}>
    <Router>
      <Home path="/" />
      <Dash path="dashboard" />
      <Admin path="/admin/*" />
    </Router>
  </ApolloProvider>
);
