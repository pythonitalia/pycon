import * as React from 'react';

import * as styles from './style.css';

interface Props {
  children?: React.ReactNode;
  title?: string;
}

export const Card = (props: Props) => {
  const { title, children } = props;

  return (
    <div className={styles.card}>
      {title && (
        <div className={styles.cardTitle}>
          <h2>{title}</h2>
        </div>
      )}

      {children}
    </div>
  );
};
