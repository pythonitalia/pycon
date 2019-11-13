import { Box, Grid, Text } from "@theme-ui/components";
import { useQuery } from "@apollo/react-hooks";
import { Redirect, RouteComponentProps } from "@reach/router";
import React, { useContext } from "react";
import { Helmet } from "react-helmet";
import { FormattedMessage } from "react-intl";
import { useLoginState } from "../../app/profile/hooks";
import { ConferenceContext } from "../../context/conference";
import {
  UserProfileQuery,
  ConferencePretixQuery,
  ConferencePretixQueryVariables,
} from "../../generated/graphql-backend";

import USER_PROFILE_QUERY from "./user-profile.graphql";
import CONFERENCE_PRETIX_EVENT from "./conference-pretix.graphql";

type Props = {
  lang: string;
};

export const TicketsForm: React.SFC<RouteComponentProps<Props>> = ({
  lang,
}) => {
  const [loggedIn] = useLoginState(false);

  if (!loggedIn) {
    return <Redirect to={`/${lang}/login`} noThrow={true} />;
  }

  const conferenceCode = useContext(ConferenceContext);

  const {
    loading: conferenceLoading,
    error: conferenceError,
    data: conferenceData,
  } = useQuery<ConferencePretixQuery, ConferencePretixQueryVariables>(
    CONFERENCE_PRETIX_EVENT,
    {
      variables: {
        conference: conferenceCode,
      },
    },
  );

  const { loading, error, data: profileData } = useQuery<UserProfileQuery>(
    USER_PROFILE_QUERY,
  );

  return (
    <Box>
      <Helmet>
        <title>Tickets</title>

        {conferenceData && (
          <link
            rel="stylesheet"
            type="text/css"
            href={`${conferenceData.conference.pretixEventUrl}/widget/v1.css`}
          />
        )}

        <script
          type="text/javascript"
          src="https://pretix.eu/widget/v1.en.js"
          async={true}
        />
      </Helmet>

      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
        }}
      >
        <Text as="h1">
          <FormattedMessage id="tickets.header" />
        </Text>

        {conferenceLoading && !conferenceError && <p>Please wait 🕐</p>}
        {!conferenceLoading && profileData && (
          <pretix-widget
            data-email={profileData.me.email}
            data-question-userid={profileData.me.id}
            event={conferenceData.conference.pretixEventUrl}
            skip-ssl-check={true}
          />
        )}
      </Box>
    </Box>
  );
};
