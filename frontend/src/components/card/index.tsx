import * as React from 'react';

import * as styles from './style.css';

type Props = {
  children: React.ReactNode;
  title: string;
};

export const Card = (props: Props) => {
  const { title, children } = props;

  return (
    <div className={styles.card}>
      <div className={styles.cardTitle}>
        <h2>{title}</h2>
      </div>

      {children}
    </div>
  );
};
