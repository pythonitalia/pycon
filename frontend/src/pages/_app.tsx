import { ApolloProvider } from "@apollo/client";
import { getMessagesForLocale } from "@python-italia/pycon-styleguide";
import "@python-italia/pycon-styleguide/custom-style";
import va from "@vercel/analytics";
import { Analytics } from "@vercel/analytics/react";
import { SpeedInsights } from "@vercel/speed-insights/next";
import { useMemo, useState } from "react";
import { RawIntlProvider, createIntl, createIntlCache } from "react-intl";

import { APOLLO_STATE_PROP_NAME, getApolloClient } from "~/apollo/client";
import { ErrorBoundary } from "~/components/error-boundary";
import { Footer } from "~/components/footer";
import { Header } from "~/components/header";
import { ModalRenderer } from "~/components/modal-renderer";
import {
  type ModalID,
  type ModalProps,
  ModalStateContext,
} from "~/components/modal/context";
import messages from "~/locale";
import { LocaleProvider, useCurrentLanguage } from "~/locale/context";
import { theme } from "~/theme";

import "../global.css";

const intlCache = createIntlCache();

const MyApp = (props) => {
  const { Component, pageProps, router, err } = props;
  const [modalData, setCurrentModalData] = useState<{
    modalId: ModalID | null;
    props?: ModalProps[keyof ModalProps];
  }>({ modalId: null });
  const apolloClient = getApolloClient(props.pageProps[APOLLO_STATE_PROP_NAME]);
  const locale = useCurrentLanguage();

  const setCurrentModal = <T extends ModalID>(
    modalId: T,
    props?: ModalProps[T],
  ) => {
    if (modalId !== null) {
      va.track("open-modal", {
        modalId,
      });
    }
    setCurrentModalData({
      modalId,
      props,
    });
  };

  const modalContext = useMemo(
    () => ({
      modalId: modalData.modalId,
      modalProps: modalData.props,
      setCurrentModal,
      closeCurrentModal: () => setCurrentModal(null),
    }),
    [modalData, setCurrentModal],
  );

  const intl = createIntl(
    {
      locale,
      messages: {
        ...messages[locale],
        ...getMessagesForLocale(locale),
      },
    },
    intlCache,
  );

  if (router.pathname === "/badge") {
    return (
      <div className="flex">
        <Component {...pageProps} err={err} />
      </div>
    );
  }
  return (
    <ApolloProvider client={apolloClient}>
      <RawIntlProvider value={intl}>
        <LocaleProvider lang={locale}>
          <SpeedInsights />
          <div className="flex flex-col min-h-screen">
            <ErrorBoundary>
              <ModalStateContext.Provider value={modalContext}>
                <Header />

                <div>
                  <Component {...pageProps} err={err} />
                  <ModalRenderer />
                  <Analytics />
                </div>

                <Footer />
              </ModalStateContext.Provider>
            </ErrorBoundary>
          </div>
        </LocaleProvider>
      </RawIntlProvider>
    </ApolloProvider>
  );
};

export default MyApp;
