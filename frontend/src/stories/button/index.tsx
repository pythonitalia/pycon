import React from 'react';
import { storiesOf } from '@storybook/react';

import { Button, ButtonLink } from '../../components/button';

storiesOf('Button', module)
  .add('default', () => <Button>Hello world</Button>)
  .add('secondary', () => <Button variant="secondary">Hello world</Button>)
  .add('link default', () => <ButtonLink>Hello world</ButtonLink>);
