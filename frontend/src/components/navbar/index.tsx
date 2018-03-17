import React from 'react';

import { Menu } from 'react-feather';
import { Box } from '../box';
import { Logo } from '../logo';
import { ButtonLink } from '../button';

export class Navbar extends React.Component<{}, {}> {
  render() {
    return (
      <Box p={3} flexDirection="row" display="flex" alignItems="center">
        <Box p={2}>
          <Menu />
        </Box>

        <Logo />

        <ButtonLink
          href="/"
          style={{
            marginLeft: 'auto'
          }}
        >
          Tickets
        </ButtonLink>
      </Box>
    );
  }
}
