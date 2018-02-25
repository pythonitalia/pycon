import { configure, addDecorator as add } from '@storybook/react';

import 'modern-normalize';

import { wrapper } from './wrapper';

function loadStories() {
  require('../src/stories/index.tsx');
  require('../src/stories/navbar/index.tsx');
  require('../src/stories/logo/index.tsx');
  require('../src/stories/box/index.tsx');
}

add(wrapper());

configure(loadStories, module);
