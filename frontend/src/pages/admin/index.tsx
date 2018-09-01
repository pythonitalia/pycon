import * as React from 'react';
import { Router, RouteComponentProps } from '@reach/router';

import * as styles from './style.css';

import { Home } from './home';
import { Logo } from '../../components/logo/index';

export const Admin = (props: RouteComponentProps) => (
  <>
    <header className={styles.header}>
      <Logo />
      <h1 className={styles.headerTitle}>Python Italia</h1>
    </header>

    <Router>
      <Home path="/" />
    </Router>
  </>
);
