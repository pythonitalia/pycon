import React from 'react';
import { storiesOf } from '@storybook/react';

import { Box } from '../../components/box';
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
    <Box flexWrap="wrap" display="flex">
      <Box px={2} py={1} width={1 / 2}>
        <Bar />
        1/2
      </Box>
      <Box px={2} py={1} width={1 / 2}>
        <Bar />
        1/2
      </Box>

      <Box px={2} py={1} width={1 / 3}>
        <Bar />
        1/3
      </Box>
      <Box px={2} py={1} width={1 / 3}>
        <Bar />
        1/3
      </Box>
      <Box px={2} py={1} width={1 / 3}>
        <Bar />
        1/3
      </Box>

      <Box px={2} py={1} width={1 / 4}>
        <Bar />
        1/4
      </Box>
      <Box px={2} py={1} width={1 / 4}>
        <Bar />
        1/4
      </Box>
      <Box px={2} py={1} width={1 / 4}>
        <Bar />
        1/4
      </Box>
      <Box px={2} py={1} width={1 / 4}>
        <Bar />
        1/4
      </Box>

      <Box px={2} py={1} width={1 / 5}>
        <Bar />
        1/5
      </Box>
      <Box px={2} py={1} width={1 / 5}>
        <Bar />
        1/5
      </Box>
      <Box px={2} py={1} width={1 / 5}>
        <Bar />
        1/5
      </Box>
      <Box px={2} py={1} width={1 / 5}>
        <Bar />
        1/5
      </Box>
      <Box px={2} py={1} width={1 / 5}>
        <Bar />
        1/5
      </Box>

      <Box px={2} py={1} width={1 / 6}>
        <Bar />
        1/6
      </Box>
      <Box px={2} py={1} width={1 / 6}>
        <Bar />
        1/6
      </Box>
      <Box px={2} py={1} width={1 / 6}>
        <Bar />
        1/6
      </Box>
      <Box px={2} py={1} width={1 / 6}>
        <Bar />
        1/6
      </Box>
      <Box px={2} py={1} width={1 / 6}>
        <Bar />
        1/6
      </Box>
      <Box px={2} py={1} width={1 / 6}>
        <Bar />
        1/6
      </Box>
    </Box>
  ))
  .add('golden ratio', () => (
    <Box flexWrap="wrap" display="flex">
      <Box p={2} width={(1 + Math.sqrt(5)) / 2 - 1}>
        <Title level={1}>Golden</Title>
        <Bar />
      </Box>
      <Box p={2} width={1 - ((1 + Math.sqrt(5)) / 2 - 1)}>
        <Title level={1}>Ratio</Title>
        <Bar />
      </Box>
    </Box>
  ));
