/** @jsx jsx */
import { RouteComponentProps } from "@reach/router";
import { Box, Button, Grid, Text } from "@theme-ui/components";
import React, { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { MetaTags } from "../meta-tags";

const SucceedUnsubscribe = () => (
  <Fragment>
    <Box
      sx={{
        maxWidth: "container",
        mx: "auto",
        my: 4,
        px: 3,
      }}
    >
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
    </Box>
  </Fragment>
);

export const UnsubscribePage: React.SFC<RouteComponentProps> = ({
  location,
}) => {
  const unsubscribed = false;
  if (unsubscribed) {
    return <SucceedUnsubscribe />;
  }

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
        as="form"
        method="post"
        onSubmit={(e: React.FormEvent<HTMLFormElement>) => {
          e.preventDefault();
          console.log("unsubscribe me :(");
        }}
      >
        <Text as="h1">
          <FormattedMessage id="unsubscribe.title" />
        </Text>
        <Button size="medium" palette="primary" type="submit">
          <FormattedMessage id="unsubscribe.button" />
        </Button>
      </Box>
    </Fragment>
  );
};
