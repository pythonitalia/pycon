import { ApolloProvider } from "@apollo/client";
import { getMessagesForLocale } from "@python-italia/pycon-styleguide";
import "@python-italia/pycon-styleguide/custom-style";
import { Router } from "next/router";
import posthog from "posthog-js";
import { PostHogProvider } from "posthog-js/react";
import { useEffect, useMemo, useState } from "react";
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

  useEffect(() => {
    try {
      posthog.init(process.env.POSTHOG_KEY, {
        api_host: "/ingest",
        ui_host: "https://eu.posthog.com",
        person_profiles: "identified_only",
        api_transport: "fetch",
        persistence: "localStorage",
        debug: process.env.NODE_ENV === "development",
      });
    } catch (error) {
      console.log("error", error);
    }

    const handleRouteChange = () => posthog?.capture("$pageview");

    Router.events.on("routeChangeComplete", handleRouteChange);
    return () => {
      Router.events.off("routeChangeComplete", handleRouteChange);
    };
  }, []);

  const setCurrentModal = <T extends ModalID>(
    modalId: T,
    props?: ModalProps[T],
  ) => {
    if (modalId !== null) {
      posthog.capture("open-modal", {
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
      <PostHogProvider client={posthog}>
        <RawIntlProvider value={intl}>
          <LocaleProvider lang={locale}>
            <div className="flex flex-col min-h-screen">
              <ErrorBoundary>
                <ModalStateContext.Provider value={modalContext}>
                  <Header />

                  <div>
                    <Component {...pageProps} err={err} />
                    <ModalRenderer />
                  </div>

                  <Footer />
                </ModalStateContext.Provider>
              </ErrorBoundary>
            </div>
          </LocaleProvider>
        </RawIntlProvider>
      </PostHogProvider>
    </ApolloProvider>
  );
};

export default MyApp;
