/** @jsx jsx */

import { useRouter } from "next/router";
import React, { Fragment, useEffect, useState } from "react";
import { FormattedMessage } from "react-intl";
import { Box, jsx, Text } from "theme-ui";

import { Alert } from "~/components/alert";
import { MetaTags } from "~/components/meta-tags";
import { useUnsubscribeMutation } from "~/types";

export const UnsubscribePage: React.SFC = () => {
  const router = useRouter();
  const email = router.query.email as string;

  const [unsubscribeEmail, { loading, error, data }] = useUnsubscribeMutation();

  useEffect(() => {
    if (!email) {
      return;
    }

    unsubscribeEmail({
      variables: {
        email,
      },
    });
  }, []);

  return (
    <Fragment>
      <FormattedMessage id="unsubscribe.title">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>

      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          my: 4,
          px: 3,
        }}
      >
        {loading && (
          <Alert variant="info">
            <FormattedMessage id="profile.loading" />
          </Alert>
        )}

        {!loading &&
          data &&
          data.unsubscribeToNewsletter.__typename ===
            "UnsubscribeToNewsletterErrors" && (
            <Alert variant="alert">{data.unsubscribeToNewsletter.email}</Alert>
          )}

        {!loading && error && !data && <Alert variant="alert">ops</Alert>}

        {!loading &&
          data &&
          data.unsubscribeToNewsletter.__typename === "OperationResult" &&
          data.unsubscribeToNewsletter.ok && (
            <Fragment>
              <Text as="h1">
                <FormattedMessage id="unsubscribe.succeed.title" />
              </Text>

              <Text
                sx={{
                  mt: 4,
                  fontSize: 2,
                }}
                as="p"
              >
                <FormattedMessage id="unsubscribe.succeed.message" />
              </Text>
            </Fragment>
          )}
      </Box>
    </Fragment>
  );
};

export default UnsubscribePage;
