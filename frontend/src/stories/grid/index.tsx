import React from 'react';
import { storiesOf } from '@storybook/react';

import { Grid, Column } from '../../components/grid';
import styled from '../../styled';
import { Title } from '../../components/typography';

const Bar = styled.hr`
  margin: 0;
  border: 0;
  height: 3px;
  background-image: linear-gradient(90deg, rgb(0, 255, 255), rgb(255, 0, 255));
`;

storiesOf('Grid', module)
  .add('simple', () => (
    <Grid>
      <Column width={1 / 2}>
        <Bar />
        1/2
      </Column>
      <Column width={1 / 2}>
        <Bar />
        1/2
      </Column>

      <Column width={1 / 3}>
        <Bar />
        1/3
      </Column>
      <Column width={1 / 3}>
        <Bar />
        1/3
      </Column>
      <Column width={1 / 3}>
        <Bar />
        1/3
      </Column>

      <Column width={1 / 4}>
        <Bar />
        1/4
      </Column>
      <Column width={1 / 4}>
        <Bar />
        1/4
      </Column>
      <Column width={1 / 4}>
        <Bar />
        1/4
      </Column>
      <Column width={1 / 4}>
        <Bar />
        1/4
      </Column>

      <Column width={1 / 5}>
        <Bar />
        1/5
      </Column>
      <Column width={1 / 5}>
        <Bar />
        1/5
      </Column>
      <Column width={1 / 5}>
        <Bar />
        1/5
      </Column>
      <Column width={1 / 5}>
        <Bar />
        1/5
      </Column>
      <Column width={1 / 5}>
        <Bar />
        1/5
      </Column>

      <Column width={1 / 6}>
        <Bar />
        1/6
      </Column>
      <Column width={1 / 6}>
        <Bar />
        1/6
      </Column>
      <Column width={1 / 6}>
        <Bar />
        1/6
      </Column>
      <Column width={1 / 6}>
        <Bar />
        1/6
      </Column>
      <Column width={1 / 6}>
        <Bar />
        1/6
      </Column>
      <Column width={1 / 6}>
        <Bar />
        1/6
      </Column>
    </Grid>
  ))
  .add('golden ratio', () => (
    <Grid>
      <Column width={(1 + Math.sqrt(5)) / 2 - 1}>
        <Title level={1}>Golden</Title>
        <Bar />
      </Column>
      <Column width={1 - ((1 + Math.sqrt(5)) / 2 - 1)}>
        <Title level={1}>Ratio</Title>
        <Bar />
      </Column>
    </Grid>
  ));
