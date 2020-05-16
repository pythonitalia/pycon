/** @jsx jsx */
import React, { Fragment, useEffect, useState } from "react";
import { FormattedMessage } from "react-intl";
import { Box, jsx, Text } from "theme-ui";

import { useUnsubscribeMutation } from "~/types";

import { Alert } from "../alert";
import { MetaTags } from "../meta-tags";

export const UnsubscribePage: React.SFC = () => {
  const [unsubscribed, setUnsubscribed] = useState(false);

  //  TODO
  const email = "TODO";

  const [unsubscribe, { loading, error, data }] = useUnsubscribeMutation({
    onCompleted(unsubscribeData) {
      if (
        unsubscribeData?.unsubscribeToNewsletter.__typename ===
          "OperationResult" &&
        unsubscribeData.unsubscribeToNewsletter.ok
      ) {
        setUnsubscribed(true);
      }
    },
  });

  useEffect(() => {
    if (!unsubscribed && email) {
      unsubscribe({
        variables: {
          email,
        },
      });
    }
  });

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

        {unsubscribed && (
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
