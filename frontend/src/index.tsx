import React from 'react';
import ReactDOM from 'react-dom';
import { ThemeProvider } from 'styled-components';

import { HomePage } from './pages/home';
import { theme } from './theme';

import 'reset-css';

ReactDOM.render(
  <ThemeProvider theme={theme}>
    <HomePage />
  </ThemeProvider>,
  document.getElementById('root') as HTMLElement,
);
