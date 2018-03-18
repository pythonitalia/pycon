import React from 'react';

import { Menu } from 'react-feather';
import { Box } from '../box';
import { Logo } from '../logo';
import { ButtonLink } from '../button';
import { Link } from '../link';

export class Navbar extends React.Component<{}, {}> {
  render() {
    return (
      <Box p={3} flexDirection="row" display="flex" alignItems="center">
        <Box p={2} display={['block', 'none']}>
          <Menu />
        </Box>

        <Logo />

        <Box ml="auto" flexDirection="row" display="flex" alignItems="center">
          <Box mr={3} display={['none', 'block']}>
            <Link href="/">Schedule</Link>
            <Link href="/">Speaker</Link>
            <Link href="/">FAQ</Link>
          </Box>
          <ButtonLink href="/">Tickets</ButtonLink>
        </Box>
      </Box>
    );
  }
}
