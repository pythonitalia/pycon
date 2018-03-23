import React from 'react';
import { storiesOf } from '@storybook/react';

import { Card } from '../../components/card';
import { Box } from 'components/box';

storiesOf('Card', module).add('default', () => (
  <Box p={4}>
    <Card>Hello world</Card>
  </Box>
));
