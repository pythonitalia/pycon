import { Fragment } from "react";
import { FormattedMessage } from "react-intl";

import { MetaTags } from "~/components/meta-tags";
import { SignupForm } from "~/components/signup-form";

export const SignupPage = () => (
  <Fragment>
    <FormattedMessage id="signup.title">
      {(title) => <MetaTags title={title} />}
    </FormattedMessage>

    <SignupForm />
  </Fragment>
);

export default SignupPage;
