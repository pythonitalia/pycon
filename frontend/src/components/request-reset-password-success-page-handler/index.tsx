import { Text, Heading, Page, Spacer } from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { LoginFlowLayout } from "../login-flow-layout";
import { MetaTags } from "../meta-tags";

export const RequestResetPasswordSuccessPageHandler = () => {
  return (
    <Page endSeparator={false}>
      <FormattedMessage id="requestResetPasswordSuccess.title">
        {(title) => <MetaTags title={title} />}
      </FormattedMessage>

      <LoginFlowLayout illustration="email">
        <Heading size="display2">
          <FormattedMessage id="requestResetPasswordSuccess.heading" />
        </Heading>
        <Spacer size="2md" />
        <Heading size={2}>
          <FormattedMessage id="requestResetPasswordSuccess.subheading" />
        </Heading>
        <Spacer size="medium" />
        <Text size={1}>
          <FormattedMessage id="requestResetPasswordSuccess.body" />
        </Text>
      </LoginFlowLayout>
    </Page>
  );
};
