import { graphql } from "gatsby";
import { Column, Row } from "grigliata";
import * as React from "react";

import { LoginForm } from "../components/login-form";
import { MaxWidthWrapper } from "../components/max-width-wrapper";
import { STANDARD_ROW_PADDING } from "../config/spacing";
import { HomePageQuery } from "../generated/graphql";
import { MainLayout } from "../layouts/main";

export default ({
  data,
  pageContext,
}: {
  data: HomePageQuery;
  pageContext: { language: string };
}) => {
  const {
    backend: { conference },
  } = data;

  return (
    <MainLayout language={pageContext.language}>
      <MaxWidthWrapper>
        <Row
          paddingLeft={STANDARD_ROW_PADDING}
          paddingRight={STANDARD_ROW_PADDING}
        >
          <Column
            columnWidth={{
              mobile: 12,
              tabletPortrait: 6,
              tabletLandscape: 6,
              desktop: 6,
            }}
          >
            <h1>Login</h1>

            <LoginForm />
          </Column>
        </Row>
      </MaxWidthWrapper>
    </MainLayout>
  );
};

export const query = graphql`
  query LoginQuery($language: String!) {
    backend {
      conference {
        introTitle: copy(key: "intro-title-1", language: $language)
        introText: copy(key: "intro-text-1", language: $language)
        introTitle2: copy(key: "intro-title-2", language: $language)
        introText2: copy(key: "intro-text-2", language: $language)
        eventsIntro: copy(key: "events-intro", language: $language)
      }
    }
  }
`;
