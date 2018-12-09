import * as React from 'react';

import { Box } from '@hackclub/design-system';

import styled from 'styled-components';

const Svg = styled(Box.withComponent('svg'))`
  width: 150px;
  background-color: ${props => props.theme.colors.accent};
  border-radius: 10px;

  > g {
    fill: ${props => props.theme.colors.primary};
  }
`;

const Logo = () => (
  <Svg viewBox="0 0 360 360" mb={6}>
    <g fillRule="evenodd">
      <text fontFamily="Varela Round" fontSize={28.496} letterSpacing={0.085}>
        <tspan x={60.108} y={292.588}>
          {'PYTHON ROMA'}
        </tspan>
      </text>
      <path d="M188.685 52.159c-28.382 0-51.472 23.089-51.472 51.47v28.742a6.872 6.872 0 0 0 6.871 6.87 6.872 6.872 0 0 0 6.873-6.87v-28.742c0-20.802 16.924-37.726 37.728-37.726 23.916 0 43.37 19.456 43.37 43.372 0 23.915-19.454 43.372-43.37 43.372h-44.6c-24.199 0-43.883 19.686-43.883 43.883v21.18c0 13.994 11.383 25.378 25.377 25.378 13.995 0 25.378-11.384 25.378-25.377v-31.396a6.873 6.873 0 1 0-13.744 0v31.396c0 6.414-5.219 11.633-11.633 11.633-6.416 0-11.635-5.22-11.635-11.633V196.53c0-16.62 13.52-30.14 30.14-30.14h44.6c31.494 0 57.114-25.622 57.114-57.115 0-31.494-25.62-57.116-57.114-57.116" />
    </g>
  </Svg>
);

export default Logo;
