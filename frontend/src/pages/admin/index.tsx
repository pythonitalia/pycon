import * as React from 'react';
import { Router, RouteComponentProps } from '@reach/router';

import * as styles from './style.css';

import { Home } from './home';
import { Members } from './members';
import { Logo } from '../../components/logo/index';
import { User } from '../../components/user/index';
import { Container, Sizes } from '../../components/container/index';

export const Admin = (props: RouteComponentProps) => (
  <>
    <header className={styles.headerWrapper}>
      <Container className={styles.header} size={Sizes.large}>
        <Logo />
        <h1 className={styles.headerTitle}>Python Italia</h1>

        <User>
          {user => <div className={styles.user}>{`hi ${user.email}`}</div>}
        </User>
      </Container>
    </header>

    <div className={styles.container}>
      <Container size={Sizes.large}>
        <Router>
          <Members path="/members" />
          <Members path="/members/:page" />
          <Home path="/" />
        </Router>
      </Container>
    </div>
  </>
);
