import React from 'react';
import { storiesOf } from '@storybook/react';

import styled from '../../styled';
import { Grid, Column } from '.';

const Bar = styled.hr`
  margin: 0;
  border: 0;
  height: 3px;
  background-image: linear-gradient(90deg, rgb(0, 255, 255), rgb(255, 0, 255));
`;

storiesOf('Grid', module).add('simple', () => (
  <Grid>
    <Column cols={6}>
      <Bar />
      1/2
    </Column>
    <Column cols={6}>
      <Bar />
      1/2
    </Column>

    <Column cols={4}>
      <Bar />
      1/3
    </Column>
    <Column cols={4}>
      <Bar />
      1/3
    </Column>
    <Column cols={4}>
      <Bar />
      1/3
    </Column>

    <Column cols={3}>
      <Bar />
      1/4
    </Column>
    <Column cols={3}>
      <Bar />
      1/4
    </Column>
    <Column cols={3}>
      <Bar />
      1/4
    </Column>
    <Column cols={3}>
      <Bar />
      1/4
    </Column>

    <Column cols={2}>
      <Bar />
      1/6
    </Column>
    <Column cols={2}>
      <Bar />
      1/6
    </Column>
    <Column cols={2}>
      <Bar />
      1/6
    </Column>
    <Column cols={2}>
      <Bar />
      1/6
    </Column>
    <Column cols={2}>
      <Bar />
      1/6
    </Column>
    <Column cols={2}>
      <Bar />
      1/6
    </Column>
  </Grid>
));
