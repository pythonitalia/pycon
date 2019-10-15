import { RouteComponentProps } from "@reach/router";
import * as React from "react";
import { Helmet } from "react-helmet";
import { FormattedMessage } from "react-intl";
import styled from "styled-components";

const Wrapper = styled.div``;

export const TicketsApp: React.SFC<RouteComponentProps> = () => (
  <>
    <Helmet>
      <title>lol</title>
      <link
        rel="stylesheet"
        type="text/css"
        href="https://pretix.eu/demo/democon/widget/v1.css"
      />

      <script
        type="text/javascript"
        src="https://pretix.eu/widget/v1.en.js"
        async={true}
      />
    </Helmet>

    <h1>
      <FormattedMessage id="profile.header" />
    </h1>

    <Wrapper>
      <pretix-widget
        data-email="test@example.org"
        event="https://pretix.eu/demo/democon/"
        skip-ssl-check={true}
      />
    </Wrapper>
  </>
);
