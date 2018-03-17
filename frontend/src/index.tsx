import * as React from 'react';
import * as ReactDOM from 'react-dom';
import App from './App';

import { ThemeProvider } from 'emotion-theming';

import { theme } from './theme';

import 'reset-css';

ReactDOM.render(
  <ThemeProvider theme={theme}>
    <App />
  </ThemeProvider>,
  document.getElementById('root') as HTMLElement
);
