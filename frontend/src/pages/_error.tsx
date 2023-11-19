import { Heading, Page, Section } from "@python-italia/pycon-styleguide";
import * as Sentry from "@sentry/nextjs";

import { GetStaticProps } from "next";
import NextErrorComponent from "next/error";

import { getApolloClient, addApolloState } from "~/apollo/client";
import { prefetchSharedQueries } from "~/helpers/prefetch";

const ErrorPage = ({ statusCode }) => (
  <Page>
    <Section>
      <Heading size={4}>Ops {statusCode}</Heading>
    </Section>

    <video
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        height: "100vh",
        width: "100vw",
        zIndex: -1,
        pointerEvents: "none",
        objectFit: "cover",
        opacity: 0.5,
      }}
      src="/videos/sad.mp4"
      autoPlay={true}
      muted={true}
      loop={true}
    />
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
