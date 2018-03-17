import React from 'react';

import { Menu } from 'react-feather';
import { Box } from '../box';

export class Navbar extends React.Component<{}, {}> {
  render() {
    return (
      <Box p={3}>
        <Menu />
      </Box>
    );
  }
}
