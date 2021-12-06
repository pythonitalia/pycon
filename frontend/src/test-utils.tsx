import { MockedProvider as OriginalMockedProvider, MockedProviderProps } from "@apollo/client/testing";
import {
  render as originalRender,
  RenderOptions,
} from "@testing-library/react";
import React, { ReactElement } from "react";
import { createIntl, createIntlCache, RawIntlProvider } from "react-intl";

import messages from "~/locale";

const Providers = ({ children }) => {
  const locale = "en";
  const intl = createIntl(
    {
      locale,
      messages: messages[locale],
    },
    createIntlCache(),
  );

  return <RawIntlProvider value={intl}>{children}</RawIntlProvider>;
};

export const render = (
  ui: ReactElement,
  options?: Omit<RenderOptions, "queries">,
) => originalRender(ui, { wrapper: Providers, ...options });

export const MockedProvider = ({ children, ...rest }: MockedProviderProps) => (
  <OriginalMockedProvider mocks={[]} addTypename {...rest}>
    {children}
  </OriginalMockedProvider>
);

export const wait = (ms: number): Promise<void> =>
  new Promise((resolve) => setTimeout(resolve, ms));

export { act, fireEvent, screen, waitFor } from "@testing-library/react";
export { default as userEvent } from "@testing-library/user-event";
