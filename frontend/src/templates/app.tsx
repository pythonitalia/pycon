/** @jsx jsx */
import { Router } from "@reach/router";
import { jsx } from "theme-ui";

import { PrivateRoute } from "../app/private-route/private-route";
import { ProfileApp } from "../app/profile";
import { EditProfileApp } from "../app/profile-edit";
import { CFPPage } from "../components/cpf-page";
import { EditSubmission } from "../components/edit-submission";
import { LoginForm } from "../components/login-form";
import { RankingPage } from "../components/ranking-page";
import { RequestPasswordReset } from "../components/request-reset-password";
import { ResetPassword } from "../components/reset-password";
import { SignupForm } from "../components/signup-form";
import { SocialLoginSuccess } from "../components/social-login-success";
import { TicketsPage } from "../components/tickets-page";
import { UnsubscribePage } from "../components/unsubscribe";
import { VotingPage } from "../components/voting-page";
import { GrantScreen } from "../screens/grants";
import { OrderConfirmationScreen } from "../screens/order-confirmation";
import { ScheduleScreen } from "../screens/schedule";
import { SubmissionPage } from "./submission";

export default () => (
  <Router>
    <PrivateRoute path="/:lang/profile" component={ProfileApp} />
    <PrivateRoute path="/:lang/profile/edit" component={EditProfileApp} />
    <SubmissionPage path="/:lang/submission/:id" />
    <PrivateRoute
      path="/:lang/submission/:id/edit"
      component={EditSubmission}
    />
    <CFPPage path="/:lang/cfp" />
    <ScheduleScreen path="/:lang/schedule" />
    <LoginForm path="/:lang/login" />
    <GrantScreen path="/:lang/grants" />
    <SocialLoginSuccess path="/:lang/login/success/" />
    <SignupForm path="/:lang/signup" />
    <RequestPasswordReset path="/:lang/reset-password/" />
    <ResetPassword path="/:lang/reset-password/:userId/:token/" />
    <UnsubscribePage path="/:lang/unsubscribe/:email" />
    <TicketsPage path="/:lang/tickets/*" />
    <PrivateRoute
      path="/:lang/orders/:code/confirmation"
      component={OrderConfirmationScreen}
    />
    <VotingPage path="/:lang/voting/" />
    <RankingPage path="/:lang/ranking/" />
  </Router>
);
