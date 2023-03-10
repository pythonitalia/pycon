import {
  Text,
  Heading,
  Page,
  Spacer,
  BasicButton,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { useCurrentLanguage } from "~/locale/context";

import { createHref } from "../link";
import { LoginFlowLayout } from "../login-flow-layout";
import { MetaTags } from "../meta-tags";

export const ResetPasswordSuccessPageHandler = () => {
  const language = useCurrentLanguage();
  return (
    <Page endSeparator={false}>
      <FormattedMessage id="resetPasswordSuccess.title">
        {(title) => <MetaTags title={title} />}
      </FormattedMessage>

      <LoginFlowLayout illustration="none">
        <Heading size="display2">
          <FormattedMessage id="resetPasswordSuccess.heading" />
        </Heading>
        <Spacer size="large" />
        <Heading size={2}>
          <FormattedMessage id="resetPasswordSuccess.subheading" />
        </Heading>
        <Spacer size="medium" />
        <Text size={1}>
          <FormattedMessage id="resetPasswordSuccess.body" />
        </Text>
        <Spacer size="medium" />
        <BasicButton
          href={createHref({
            path: "/login",
            locale: language,
          })}
        >
          <FormattedMessage id="requestResetPassword.backToLogin.login" />
        </BasicButton>
      </LoginFlowLayout>
    </Page>
  );
};
