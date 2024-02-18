import {
  BasicButton,
  Button,
  Heading,
  Link,
  Page,
  Section,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";

import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Alert } from "~/components/alert";
import { PageLoading } from "~/components/page-loading";
import { useLoginState } from "~/components/profile/hooks";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useOrderQuery } from "~/types";

const OrderCanceled = () => (
  <React.Fragment>
    <Heading size={1}>
      <FormattedMessage id="orderConfirmation.heading.canceled" />
    </Heading>
    <Spacer size="xs" />
    <Text as="p">
      <FormattedMessage id="orderConfirmation.tryAgain" />
    </Text>
    <Spacer size="medium" />
    <Button href="/tickets">
      <FormattedMessage id="orderConfirmation.tickets" />
    </Button>
  </React.Fragment>
);

const OrderSucceeded = ({ url }: { url: string }) => (
  <React.Fragment>
    <Heading size={1}>
      <FormattedMessage id="orderConfirmation.heading" />
    </Heading>
    <Spacer size="xs" />
    <Text as="p">
      <FormattedMessage id="orderConfirmation.successMessage" />
    </Text>
    <Spacer size="xs" />
    <Button href="/">
      <FormattedMessage id="orderConfirmation.home" />
    </Button>
    <Spacer size="medium" />
    <BasicButton href={url}>
      <FormattedMessage id="orderConfirmation.manage" />
    </BasicButton>
  </React.Fragment>
);

const OrderPending = ({ url, code }: { url: string; code: string }) => (
  <React.Fragment>
    <Heading size={1}>
      <FormattedMessage id="orderConfirmation.heading.pending" />
    </Heading>
    <Spacer size="xs" />
    <Text as="p">
      <FormattedMessage id="orderConfirmation.pendingMessage" />
    </Text>
    <Spacer size="medium" />
    <Text as="p">
      <FormattedMessage id="orderConfirmation.cardMessage" />
    </Text>
    <Spacer size="xs" />
    <Button href={url}>
      <FormattedMessage id="orderConfirmation.pendingManage" />
    </Button>
    <Spacer size="medium" />

    <Text as="p">
      <FormattedMessage
        id="orderConfirmation.bankMessage"
        values={{
          code: <Text weight="strong">{code}</Text>,
          email: (
            <Link target="_blank" href="mailto:help@pycon.it">
              help@pycon.it
            </Link>
          ),
        }}
      />
    </Text>
  </React.Fragment>
);

export const OrderConfirmationPage = () => {
  const [loggedIn, _] = useLoginState();

  const router = useRouter();
  const code = router.query.id as string;

  const { data, loading, error } = useOrderQuery({
    variables: { code, conferenceCode: process.env.conferenceCode },
    skip: !loggedIn,
  });

  if (error) {
    return (
      <Page>
        <Section>
          <Alert variant="alert">{error.message}</Alert>
        </Section>
      </Page>
    );
  }

  if (loading || !data) {
    return <PageLoading titleId="global.loading" />;
  }

  return (
    <Page>
      <Section>
        {(data.order.status === "CANCELED" ||
          data.order.status === "EXPIRED") && <OrderCanceled />}
        {data.order.status === "PAID" && (
          <OrderSucceeded url={data.order.url} />
        )}
        {data.order.status === "PENDING" && (
          <OrderPending code={code} url={data.order.url} />
        )}
      </Section>
    </Page>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await prefetchSharedQueries(client, locale);

  return addApolloState(client, {
    props: {},
  });
};

export const getStaticPaths: GetStaticPaths = async () =>
  Promise.resolve({
    paths: [],
    fallback: "blocking",
  });

export default OrderConfirmationPage;
