import { Fragment } from "react";

import { LoginForm } from "~/components/login-form";
import { MetaTags } from "~/components/meta-tags";

export default () => (
  <Fragment>
    <MetaTags title={"Login"} />

    <LoginForm />
  </Fragment>
);
