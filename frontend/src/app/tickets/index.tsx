import { useQuery } from "@apollo/react-hooks";
import { Redirect, RouteComponentProps } from "@reach/router";
import { Alert } from "fannypack";
import { graphql, useStaticQuery } from "gatsby";
import * as React from "react";
import { Helmet } from "react-helmet";
import { FormattedMessage } from "react-intl";
import styled from "styled-components";

import { useLoginState } from "../../app/profile/hooks";
import { TicketsPageQuery } from "../../generated/graphql";
import { UserProfileQuery } from "../../generated/graphql-backend";
import USER_PROFILE_QUERY from "./user-profile.graphql";

const Wrapper = styled.div``;

type Props = RouteComponentProps & {
  lang: string;
};

export const TicketsApp: React.SFC<Props> = ({ lang }) => {
  const [loggedIn, setLoggedIn] = useLoginState(false);

  const {
    backend: {
      conference: { pretixEventUrl },
    },
  } = useStaticQuery<TicketsPageQuery>(graphql`
    query TicketsPage {
      backend {
        conference {
          pretixEventUrl
        }
      }
    }
  `);

  const { loading, error, data: profileData } = useQuery<UserProfileQuery>(
    USER_PROFILE_QUERY,
  );

  if (!loggedIn) {
    return (
      <Redirect
        to={`/${lang}/login`}
        state={{ message: "You need to login to buy a ticket" }}
        noThrow={true}
      />
    );
  }

  return (
    <>
      <Helmet>
        <title>Tickets</title>
        <link
          rel="stylesheet"
          type="text/css"
          href={`${pretixEventUrl}/widget/v1.css`}
        />

        <script
          type="text/javascript"
          src="https://pretix.eu/widget/v1.en.js"
          async={true}
        />
      </Helmet>

      <h1>
        <FormattedMessage id="tickets.header" />
      </h1>

      <Wrapper>
        {loading && !error && <p>Please wait 🕐</p>}
        {!loading && error && <Alert type="danger">{error.message}</Alert>}
        {!loading && profileData && (
          <pretix-widget
            data-email={profileData.me.email}
            data-question-userid={profileData.me.id}
            event={pretixEventUrl}
            skip-ssl-check={true}
          />
        )}
      </Wrapper>
    </>
  );
};
