import React from 'react';
import { ThemeProvider } from 'styled-components';

import { theme } from '../src/theme';

export function wrapper() {
  return story => {
    return (
      <ThemeProvider theme={theme}>
        <div>{story()}</div>
      </ThemeProvider>
    );
  };
}
