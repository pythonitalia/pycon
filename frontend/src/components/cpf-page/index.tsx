/** @jsx jsx */
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { CfpForm } from "../../components/cfp-form";
import { MetaTags } from "../meta-tags";
import { Introduction } from "./introduction";

export const CFPPage = () => (
  <Fragment>
    <FormattedMessage id="cfp.pageTitle">
      {text => <MetaTags title={text} />}
    </FormattedMessage>

    <Introduction />

    <CfpForm />
  </Fragment>
);
