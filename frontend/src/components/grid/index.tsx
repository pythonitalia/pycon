import React from 'react';
import { Box } from '../box';

type ColumnProps = {
  width: number;
};

export const Column: React.SFC<ColumnProps> = ({
  width,
  children,
  ...props
}) => (
  <Box px={2} py={1} width={width} {...props}>
    {children}
  </Box>
);

export const Grid: React.SFC = ({ children, ...props }) => (
  <Box flexWrap="wrap" display="flex" {...props}>
    {children}
  </Box>
);
