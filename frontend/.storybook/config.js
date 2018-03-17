import { configure, addDecorator as add } from '@storybook/react';

import 'reset-css';

import { wrapper } from './wrapper';

function loadStories() {
  require('../src/stories/index.tsx');
  require('../src/stories/navbar/index.tsx');
  require('../src/stories/logo/index.tsx');
  require('../src/stories/box/index.tsx');
  require('../src/stories/typography/index.tsx');
  require('../src/stories/button/index.tsx');
}

add(wrapper());

configure(loadStories, module);
