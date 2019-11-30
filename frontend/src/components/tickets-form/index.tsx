import { useQuery } from "@apollo/react-hooks";
import { Redirect, RouteComponentProps } from "@reach/router";
import { Box, Grid, Text } from "@theme-ui/components";
import React, { useContext } from "react";
import { Helmet } from "react-helmet";
import { FormattedMessage } from "react-intl";

import { useLoginState } from "../../app/profile/hooks";
import { ConferenceContext } from "../../context/conference";
import {
  ConferencePretixQuery,
  ConferencePretixQueryVariables,
  UserProfileQuery,
} from "../../generated/graphql-backend";
import CONFERENCE_PRETIX_EVENT from "./conference-pretix.graphql";
import USER_PROFILE_QUERY from "./user-profile.graphql";

type Props = {
  lang: string;
};

export const TicketsForm: React.SFC<RouteComponentProps<Props>> = ({
  lang,
}) => {
  const [loggedIn] = useLoginState();

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
      <FormattedMessage id="tickets.pageTitle">
        {text => (
          <Helmet>
            <title>{text}</title>

            {conferenceData && (
              <link rel="stylesheet" type="text/css" href={`/css/pretix.css`} />
            )}

            <script
              type="text/javascript"
              src="https://d3ex7joy4im5c0.cloudfront.net/widget/v1.en.js"
              async={true}
            />
          </Helmet>
        )}
      </FormattedMessage>

      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          px: 3,
        }}
      >
        {conferenceLoading && !conferenceError && <p>Please wait 🕐</p>}
        {!conferenceLoading && profileData && (
          <pretix-widget
            data-email={profileData.me.email}
            data-question-userid={profileData.me.id}
            event={conferenceData!.conference.pretixEventUrl}
            skip-ssl-check={true}
          />
        )}
      </Box>
    </Box>
  );
};
