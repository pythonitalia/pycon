import * as React from 'react';
import { Router, RouteComponentProps } from '@reach/router';

import { Home } from './home';

export const Admin = (props: RouteComponentProps) => (
  <Router>
    <Home path="/" />
  </Router>
);
