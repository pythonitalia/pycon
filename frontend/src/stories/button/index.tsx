import React from 'react';
import { storiesOf } from '@storybook/react';

import { Button } from '../../components/button';

storiesOf('Button', module)
  .add('plain', () => <Button>Hello world</Button>);
