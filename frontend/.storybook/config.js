import { configure, addDecorator as add } from '@storybook/react';

import 'reset-css';

import { wrapper } from './wrapper';

const req = require.context('../src/components', true, /.stories.tsx$/);

function loadStories() {
    req.keys().forEach(filename => req(filename));
}

add(wrapper());

configure(loadStories, module);
