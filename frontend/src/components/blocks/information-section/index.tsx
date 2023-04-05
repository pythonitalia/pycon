import {
  Heading,
  Button,
  Countdown,
  Section,
  VerticalStack,
  Spacer,
  DynamicHTMLText,
} from "@python-italia/pycon-styleguide";
import { Color } from "@python-italia/pycon-styleguide/dist/types";
import { getIllustration } from "@python-italia/pycon-styleguide/illustrations";

import { Cta, useInformationSectionQuery } from "~/types";

type Props = {
  title: string;
  body: string;
  cta: Cta;
  illustration: string;
  countdownToDatetime: string | null;
  countdownToDeadline: string | null;
  backgroundColor: Color;
};

export const InformationSection = ({
  title,
  body,
  cta,
  countdownToDatetime,
  countdownToDeadline,
  backgroundColor,
  illustration,
}: Props) => {
  const { data } = useInformationSectionQuery({
    variables: {
      code: process.env.conferenceCode,
    },
  });
  const IllustrationComponent = getIllustration(illustration);
  const deadlineDatetime =
    countdownToDeadline && Object.hasOwn(data.conference, countdownToDeadline)
      ? new Date(data.conference[countdownToDeadline].start)
      : null;

  return (
    <Section
      spacingSize="none"
      containerSize="2md"
      background={backgroundColor}
    >
      <Spacer size="3xl" />
      <VerticalStack alignItems="center">
        <Heading size="display2" align="center">
          {title}
        </Heading>
        {body && (
          <>
            <Spacer size="large" />
            <div className="text-center">
              <DynamicHTMLText text={body} />
            </div>
          </>
        )}
        {(countdownToDatetime || deadlineDatetime) && (
          <>
            <Spacer size="large" />
            <Countdown
              background={backgroundColor === "cream" ? "milk" : "cream"}
              deadline={new Date(countdownToDatetime || deadlineDatetime)}
            />
          </>
        )}
        {cta && (
          <>
            <Spacer size="large" />
            <Button href={cta.link} role="primary">
              {cta.label}
            </Button>
          </>
        )}
        {IllustrationComponent && (
          <>
            <Spacer size="large" />
            <IllustrationComponent />
          </>
        )}
        {!IllustrationComponent && <Spacer size="3xl" />}
      </VerticalStack>
    </Section>
  );
};
