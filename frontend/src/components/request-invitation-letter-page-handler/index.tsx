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
import { DeadlineStatus, useRequestInvitationLetterPageQuery } from "~/types";
import { createHref } from "../link";
import { InvitationLetterForm } from "./invitation-letter-form";

export const RequestInvitationLetterPageHandler = () => {
  const language = useCurrentLanguage();
  const {
    data: {
      conference: { invitationLetterRequestDeadline },
      me: { hasAdmissionTicket, invitationLetterRequest },
    },
  } = useRequestInvitationLetterPageQuery({
    variables: {
      conference: process.env.conferenceCode,
    },
  });

  const deadlineStatus = invitationLetterRequestDeadline?.status;

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

        {(!deadlineStatus || deadlineStatus === DeadlineStatus.InThePast) && (
          <FormClosed />
        )}
        {deadlineStatus === DeadlineStatus.InTheFuture && (
          <FormOpeningSoon date={invitationLetterRequestDeadline?.start} />
        )}
        {deadlineStatus === DeadlineStatus.HappeningNow && (
          <InvitationLetterForm
            hasAdmissionTicket={hasAdmissionTicket}
            invitationLetterRequest={invitationLetterRequest}
          />
        )}
      </Section>
    </Page>
  );
};

const FormClosed = () => (
  <Text size={2}>
    <FormattedMessage id="requestInvitationLetter.formClosed" />
  </Text>
);

const FormOpeningSoon = ({ date }) => {
  const language = useCurrentLanguage();
  const formatter = new Intl.DateTimeFormat(language, {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
  });

  return (
    <Text size={2}>
      <FormattedMessage
        id="requestInvitationLetter.formOpeningSoon"
        values={{
          date: formatter.format(new Date(date)),
        }}
      />
    </Text>
  );
};
