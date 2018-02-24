import React from 'react';
import { storiesOf } from '@storybook/react';
import { action } from '@storybook/addon-actions';

storiesOf('Button', module)
  .add('with text', () => (
    <div onClick={action('clicked')}>Hello Button</div>
  ))
  .add('with some emoji', () => (
    <div onClick={action('clicked')}>😀 😎 👍 💯</div>
  ));
