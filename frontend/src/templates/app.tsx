import { Router } from "@reach/router";
import { Column, Row } from "grigliata";
import * as React from "react";

import { CfpForm } from "../app/cfp";
import { ProfileApp } from "../app/profile";
import { LoginForm } from "../components/login-form";
import { MaxWidthWrapper } from "../components/max-width-wrapper";
import { SignupForm } from "../components/signup-form";
import { STANDARD_ROW_PADDING } from "../config/spacing";
import { MainLayout } from "../layouts/main";

export default ({ pageContext }: { pageContext: { language: string } }) => (
  <MainLayout language={pageContext.language}>
    <MaxWidthWrapper>
      <Row
        paddingLeft={STANDARD_ROW_PADDING}
        paddingRight={STANDARD_ROW_PADDING}
      >
        <Column
          columnWidth={{
            mobile: 12,
            tabletPortrait: 12,
            tabletLandscape: 12,
            desktop: 12,
          }}
        >
          <Router>
            <ProfileApp path="/:lang/profile" />
            <LoginForm path="/:lang/login" />
            <SignupForm path="/:lang/signup" />
            <CfpForm path="/:lang/cfp" />
          </Router>
        </Column>
      </Row>
    </MaxWidthWrapper>
  </MainLayout>
);
