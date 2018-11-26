import * as React from 'react';

import * as styles from './style.css';

export const Title: React.SFC = ({ children }) => (
  <h1 className={styles.title}>{children}</h1>
);
