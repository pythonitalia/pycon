import React from 'react';
import { storiesOf } from '@storybook/react';

import { Title, Paragraph } from '.';

storiesOf('Typography', module)
  .add('titles', () => (
    <div>
      <Title level={1}>Title 1</Title>
      <Title level={2}>Title 2</Title>
      <Title level={3}>Title 3</Title>
      <Title level={4}>Title 4</Title>
      <Title level={5}>Title 5</Title>
      <Title level={6}>Title 6</Title>
    </div>
  ))
  .add('paragraphs', () => (
    <div>
      <Title level={3}>Primary (default) copy</Title>

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

      <Title level={3}>Secondary copy</Title>

      <Paragraph variant="secondary">
        Legio eligo sed medius, negotium oblivio sed neque neque culpa lacrima
        dulcis lorem, sit quis, sit infantia gratia virtus quis in trivia trivia
        benevolentia legis ergo dolor lacuna virtus insula sit canvallis caelum
        quis impera fabula lacuna lorem medius ora.
      </Paragraph>
    </div>
  ));
