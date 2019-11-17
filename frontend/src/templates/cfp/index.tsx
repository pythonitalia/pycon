/** @jsx jsx */
import { Fragment } from "react";
import { Helmet } from "react-helmet";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { CfpForm } from "../../components/cfp-form";
import { Introduction } from "./introduction";

export default () => (
  <Fragment>
    <FormattedMessage id="cfp.pageTitle">
      {text => (
        <Helmet>
          <title>{text}</title>
        </Helmet>
      )}
    </FormattedMessage>

    <Introduction />

    <CfpForm />
  </Fragment>
);
