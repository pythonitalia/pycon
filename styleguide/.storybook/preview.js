import "../src/style.css";
import {IntlProvider} from 'react-intl'

export const parameters = {
  actions: { argTypesRegex: "^on[A-Z].*" },
  layout: "fullscreen",
};

export const decorators = [
  (Story) => (
    <IntlProvider locale="en" defaultLocale="en">
      <Story />
    </IntlProvider>
  ),
];
