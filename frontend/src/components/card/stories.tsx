import React from 'react';
import { storiesOf } from '@storybook/react';

import { Box } from '../box';
import { Card } from '.';

storiesOf('Card', module)
  .add('default', () => (
    <Box p={4}>
      <Card>Hello world</Card>
    </Box>
  ))
  .add('image', () => (
    <Box p={4}>
      <Card src="https://placeimg.com/480/640/people">Hello world</Card>
    </Box>
  ));
