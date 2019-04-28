import * as React from 'react';

import { Router, RouteComponentProps } from '@reach/router';
import { ApolloProvider } from 'react-apollo';

import { Home } from '../../pages/home';
import { Admin } from '../../pages/admin';
import { Schedule } from '../../pages/schedule';

import { client } from './client';

import './base.css';
import './typography.css';

const Dash = (props: RouteComponentProps) => <div>Dash</div>;

export const App = () => (
  <ApolloProvider client={client}>
    <Router>
      <Home path="/" />
      <Schedule path="/schedule" />
      <Dash path="dashboard" />
      <Admin path="/admin/*" />
    </Router>
  </ApolloProvider>
);
