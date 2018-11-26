import * as React from 'react';
import { Section } from '@hackclub/design-system';

import styled from 'styled-components';

interface Props {
  backgroundImage: string;
}

export const Hero = styled(Section)`
  background-image: url(${(props: Props) => props.backgroundImage});
  background-size: cover;
  background-position: center;
  min-height: 45vh;

  position: relative;

  &::before {
    content: '';
    background: black;
    opacity: 0.4;
    width: 100%;
    height: 100%;
    left: 0;
    top: 0;
    position: absolute;
    z-index: 1;
    display: block;
  }

  > * {
    position: relative;
    z-index: 2;
  }
`;

Hero.defaultProps = {
  ...Section.defaultProps,
  align: 'flex-start',
  flexDirection: 'column',
  justify: 'flex-start',
  color: 'white',
};
