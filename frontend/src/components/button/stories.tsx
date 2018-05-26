import React from 'react';
import { storiesOf } from '@storybook/react';

import { Button, ButtonLink } from '.';

storiesOf('Button', module)
  .add('default', () => <Button>Hello world</Button>)
  .add('secondary', () => <Button variant="secondary">Hello world</Button>)
  .add('link default', () => <ButtonLink>Hello world</ButtonLink>);
