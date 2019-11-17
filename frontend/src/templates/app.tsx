/** @jsx jsx */
import { Router } from "@reach/router";
import { jsx } from "theme-ui";

import { PrivateRoute } from "../app/private-route/private-route";
import { ProfileApp } from "../app/profile";
import { EditProfileApp } from "../app/profile-edit";
import { LoginForm } from "../components/login-form";
import { SignupForm } from "../components/signup-form";
import { SubmissionPage } from "../components/submission-page";

export default () => (
  <Router>
    <PrivateRoute path="/:lang/profile" component={ProfileApp} />
    <PrivateRoute path="/:lang/profile-edit" component={EditProfileApp} />
    <PrivateRoute path="/:lang/submission/:id" component={SubmissionPage} />
    <LoginForm path="/:lang/login" />
    <SignupForm path="/:lang/signup" />
  </Router>
);
