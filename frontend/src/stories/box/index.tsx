import React from 'react';
import { storiesOf } from '@storybook/react';

import { Box } from '../../components/box';

storiesOf('Box', module)
  .add('plain', () => <Box>Hello world</Box>)
  .add('font size', () => <Box fontSize={4}>Hello world</Box>)
  .add('complex', () => (
    <Box m={2} p={1} boxShadow={1}>
      Hello world
    </Box>
  ))
  .add('padding', () => (
    // padding: 32px (theme.space[3])
    <Box p={3}>Hello world</Box>
  ))
  .add('color', () => (
    // color
    <Box color="tomato">Hello world </Box>
  ))
  .add('background color', () => (
    // background color
    <Box bg="tomato">Hello world</Box>
  ));
