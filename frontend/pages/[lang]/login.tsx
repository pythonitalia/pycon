import { Fragment } from "react";
import { FormattedMessage } from "react-intl";

import { LoginForm } from "~/components/login-form";
import { MetaTags } from "~/components/meta-tags";

export const LoginPage = () => (
  <Fragment>
    <FormattedMessage id="login.title">
      {(title) => <MetaTags title={title} />}
    </FormattedMessage>

    <LoginForm />
  </Fragment>
);

export default LoginPage;
