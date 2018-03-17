import React from 'react';

import {
  space,
  width,
  fontSize,
  color,
  boxShadow,
  SpaceProps,
  WidthProps,
  FontSizeProps,
  ColorProps,
  BoxShadowProps
} from 'styled-system';

import styled from '../../styled';

type BoxProps = SpaceProps &
  WidthProps &
  FontSizeProps &
  ColorProps &
  BoxShadowProps;

export const Box: React.SFC<BoxProps> = styled('div')`
  ${space}
  ${width}
  ${fontSize}
  ${color}
  ${boxShadow}
`;
