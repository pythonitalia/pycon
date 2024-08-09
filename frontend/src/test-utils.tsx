import {
  type MockedProviderProps,
  MockedProvider as OriginalMockedProvider,
} from "@apollo/client/testing";
import {
  type RenderOptions,
  render as originalRender,
} from "@testing-library/react";
import React, { type ReactElement } from "react";
import { RawIntlProvider, createIntl, createIntlCache } from "react-intl";

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
