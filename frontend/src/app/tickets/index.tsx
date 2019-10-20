import { RouteComponentProps } from "@reach/router";
import { graphql, useStaticQuery } from "gatsby";
import * as React from "react";
import { Helmet } from "react-helmet";
import { FormattedMessage } from "react-intl";
import styled from "styled-components";
import { TicketsPageQuery } from "../../generated/graphql";

const Wrapper = styled.div``;

export const TicketsApp: React.SFC<RouteComponentProps> = () => {
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
        <pretix-widget
          data-email="test@example.org"
          event={pretixEventUrl}
          skip-ssl-check={true}
        />
      </Wrapper>
    </>
  );
};
