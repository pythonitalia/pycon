import {
  Heading,
  Link,
  Page,
  Section,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";
import { MetaTags } from "~/components/meta-tags";
import { useCurrentLanguage } from "~/locale/context";
import { createHref } from "../link";
import { InvitationLetterForm } from "./invitation-letter-form";

export const RequestInvitationLetterPageHandler = () => {
  const language = useCurrentLanguage();

  return (
    <Page endSeparator={false}>
      <FormattedMessage id="requestInvitationLetter.pageTitle">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>

      <Section>
        <Heading size="display2">
          <FormattedMessage id="requestInvitationLetter.heading" />
        </Heading>

        <Spacer size="small" />

        <Link
          href={createHref({
            path: "/visa",
            locale: language,
          })}
        >
          <Text color="none" weight="strong" decoration="underline" size={2}>
            <FormattedMessage id="global.learnMore" />
          </Text>
        </Link>

        <Spacer size="xl" />

        <InvitationLetterForm />
      </Section>
    </Page>
  );
};
