import { Heading, Page, Section, Text } from "@python-italia/pycon-styleguide";
import * as Sentry from "@sentry/nextjs";

import type { GetStaticProps } from "next";
import NextErrorComponent from "next/error";
import { FormattedMessage } from "react-intl";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { prefetchSharedQueries } from "~/helpers/prefetch";

const ErrorPage = ({ statusCode }) => (
  <Page>
    <Section>
      <Heading size={4}>
        <FormattedMessage id="errorPage.title" />
      </Heading>
      <Text size={2}>
        <FormattedMessage
          id="errorPage.body"
          values={{
            reportLink: (
              <a href="https://github.com/pythonitalia/pycon/issues">
                <FormattedMessage id="errorPage.reportLink" />
              </a>
            ),
          }}
        />
      </Text>
      <img
        src="/images/ernesto.jpg"
        alt="Ernesto thinking about pineapple pizza"
        style={{ maxWidth: "100%", marginTop: "1rem" }}
      />
    </Section>
  </Page>
);

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([prefetchSharedQueries(client, locale)]);

  return addApolloState(client, {
    props: {},
  });
};

export const getInitialProps = async (contextData) => {
  // In case this is running in a serverless function, await this in order to give Sentry
  // time to send the error before the lambda exits
  await Sentry.captureUnderscoreErrorException(contextData);

  // This will contain the status code of the response
  return NextErrorComponent.getInitialProps(contextData);
};

export default ErrorPage;
