/** @jsx jsx */
import { Router } from "@reach/router";
import { jsx } from "theme-ui";

import { PrivateRoute } from "../app/private-route/private-route";
import { ProfileApp } from "../app/profile";
import { EditProfileApp } from "../app/profile-edit";
import { CFPPage } from "../components/cpf-page";
import { LoginForm } from "../components/login-form";
import { RequestPasswordReset } from "../components/request-reset-password";
import { ResetPassword } from "../components/reset-password";
import { SignupForm } from "../components/signup-form";
import { SocialLoginSuccess } from "../components/social-login-success";
import { SubmissionPage } from "../components/submission-page";

export default () => (
  <Router>
    <PrivateRoute path="/:lang/profile" component={ProfileApp} />
    <PrivateRoute path="/:lang/profile/edit" component={EditProfileApp} />
    <PrivateRoute path="/:lang/submission/:id" component={SubmissionPage} />
    <PrivateRoute path="/:lang/cfp" component={CFPPage} />
    <LoginForm path="/:lang/login" />
    <SocialLoginSuccess path="/:lang/login/success/" />
    <SignupForm path="/:lang/signup" />
    <RequestPasswordReset path="/:lang/reset-password/" />
    <ResetPassword path="/:lang/reset-password/:userId/:token/" />
  </Router>
);
