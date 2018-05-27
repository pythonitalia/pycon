import React from 'react';
import { storiesOf } from '@storybook/react';

import { Hero } from '.';
import { Button } from '../button';

storiesOf('Hero', module)
  .add('default', () => (
    <Hero src="https://images.unsplash.com/photo-1433215735557-911693026827?&w=900&q=80">
      Hello world
    </Hero>
  ))
  .add('with footer', () => (
    <Hero
      src="https://images.unsplash.com/photo-1433215735557-911693026827?&w=900&q=80"
      renderFooter={() => <Button>Hello world</Button>}
    >
      Hello world
    </Hero>
  ));
