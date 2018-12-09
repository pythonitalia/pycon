import * as React from 'react';

import { injectGlobal } from 'styled-components';
import { ThemeProvider } from '@hackclub/design-system';

import theme from '../../theme';

// tslint:disable-next-line:no-unused-expression
injectGlobal`
* {
    margin: 0;
    padding: 0;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

html {
    font-size: 62.5%;
    box-sizing: border-box;
}

*,
*:before,
*:after {
    box-sizing: inherit;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    font-size: 1.6rem;
}
`;

export const AppWrapper: React.SFC = ({ children }) => (
  <ThemeProvider webfonts theme={theme}>
    {children}
  </ThemeProvider>
);
