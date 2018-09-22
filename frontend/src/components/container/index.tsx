import * as React from 'react';
import * as styles from './style.css';

export enum Sizes {
  large = 'containerLarge',
}

type Props = {
  children: React.ReactNode;
  size: Sizes;
  className?: string;
};

export const Container: React.SFC = (props: Props) => {
  return (
    <div
      className={`${styles.container} ${styles[props.size]} ${props.className}`}
    >
      {props.children}
    </div>
  );
};

Container.defaultProps = {
  className: '',
};
