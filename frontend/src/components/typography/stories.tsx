import React from 'react';
import { storiesOf } from '@storybook/react';

import { Title, Paragraph } from '.';

storiesOf('Typography', module)
  .add('titles', () => (
    <div>
      <Title level={1}>Title 1</Title>
      <Title level={2}>Title 2</Title>
      <Title level={3}>Title 3</Title>
    </div>
  ))
  .add('paragraphs', () => (
    <div>
      <Paragraph>
        Legio eligo sed medius, negotium oblivio sed neque neque culpa lacrima
        dulcis lorem, sit quis, sit infantia gratia virtus quis in trivia trivia
        benevolentia legis ergo dolor lacuna virtus insula sit canvallis caelum
        quis impera fabula lacuna lorem medius ora.
      </Paragraph>
      <Paragraph>
        Legio eligo sed medius, negotium oblivio sed neque neque culpa lacrima
        dulcis lorem, sit quis, sit infantia gratia virtus quis in trivia trivia
        benevolentia legis ergo dolor lacuna virtus insula sit canvallis caelum
        quis impera fabula lacuna lorem medius ora.
      </Paragraph>
    </div>
  ));
