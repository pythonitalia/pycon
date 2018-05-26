import React from 'react';

import cx from 'classnames';

type ColumnProps = {
  cols?: 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12;
};

export const Column: React.SFC<ColumnProps> = ({
  cols,
  children,
  ...props
}) => {
  const classes = cx('mdc-layout-grid__cell', {
    [`mdc-layout-grid__cell--span-${cols}`]: !!cols,
  });

  return (
    <div className={classes} {...props}>
      {children}
    </div>
  );
};

export const Grid: React.SFC = ({ children, ...props }) => (
  <div className="mdc-layout-grid" {...props}>
    <div className="mdc-layout-grid__inner">{children}</div>
  </div>
);
