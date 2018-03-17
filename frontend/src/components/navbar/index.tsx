import React from 'react';

import { Menu } from 'react-feather';
import { Box } from '../box';
import { Logo } from '../logo';

export class Navbar extends React.Component<{}, {}> {
  render() {
    return (
      <Box p={3} flexDirection="row" display="flex" alignItems="center">
        <Box p={2}>
          <Menu />
        </Box>

        <Logo />
      </Box>
    );
  }
}
