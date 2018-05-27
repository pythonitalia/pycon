import React from 'react';
import { storiesOf } from '@storybook/react';

import { Hero } from '.';

storiesOf('Hero', module).add('default', () => (
  <Hero src="https://images.unsplash.com/photo-1433215735557-911693026827?&w=900&q=80">
    Hello world
  </Hero>
));
