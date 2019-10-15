import { Router } from "@reach/router";
import { Container } from "grigliata";
import * as React from "react";

import { ProfileApp } from "../app/profile";
import { TicketsApp } from "../app/tickets";
import { LoginForm } from "../components/login-form";
import { SignupForm } from "../components/signup-form";
import { MainLayout } from "../layouts/main";

export default ({ pageContext }: { pageContext: { language: string } }) => (
  <MainLayout language={pageContext.language}>
    <Container>
      <Router>
        <ProfileApp path="/:lang/profile" />
        <TicketsApp path="/:lang/tickets" />
        <LoginForm path="/:lang/login" />
        <SignupForm path="/:lang/signup" />
      </Router>
    </Container>
  </MainLayout>
);
