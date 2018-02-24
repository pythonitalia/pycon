import React from 'react';
import { storiesOf } from '@storybook/react';

import { Logo } from '../../components/logo';

storiesOf('Logo', module).add('normal', () => (
  <div
    style={{
      width: 300
    }}
  >
    <Logo />
  </div>
));
