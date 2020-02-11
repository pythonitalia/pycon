/** @jsx jsx */
import { useMutation } from "@apollo/react-hooks";
import { RouteComponentProps } from "@reach/router";
import { Box, Text } from "@theme-ui/components";
import React, { Fragment, useEffect, useState } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import {
  UnsubscribeMutation,
  UnsubscribeMutationVariables,
} from "../../generated/graphql-backend";
import { Alert } from "../alert";
import { MetaTags } from "../meta-tags";
import UNSUBSCRIBE_TO_NEWSLETTER from "./unsubscribe.graphql";

type Props = {
  lang: string;
  email?: string;
};

export const UnsubscribePage: React.SFC<RouteComponentProps<Props>> = ({
  location,
  email,
}) => {
  const [unsubscribed, setUnsubscribed] = useState(false);

  const onUnsubscribeComplete = (unsubscribeData: UnsubscribeMutation) => {
    if (
      unsubscribeData?.unsubscribeToNewsletter.__typename ===
        "OperationResult" &&
      unsubscribeData.unsubscribeToNewsletter.ok
    ) {
      setUnsubscribed(true);
    }
  };

  const [unsubscribe, { loading, error, data }] = useMutation<
    UnsubscribeMutation,
    UnsubscribeMutationVariables
  >(UNSUBSCRIBE_TO_NEWSLETTER, { onCompleted: onUnsubscribeComplete });

  useEffect(() => {
    // Update the document title using the browser API
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
        {text => <MetaTags title={text} />}
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
