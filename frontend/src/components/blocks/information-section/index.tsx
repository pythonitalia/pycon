import {
  Button,
  Countdown,
  Heading,
  Section,
  Spacer,
  StyledHTMLText,
  VerticalStack,
} from "@python-italia/pycon-styleguide";
import type { Illustration } from "@python-italia/pycon-styleguide/dist/illustrations/types";
import type { Color } from "@python-italia/pycon-styleguide/dist/types";
import { getIllustration } from "@python-italia/pycon-styleguide/illustrations";
import { type ModalID, useSetCurrentModal } from "~/components/modal/context";

import {
  type Cta,
  queryInformationSection,
  useInformationSectionQuery,
} from "~/types";

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
  const setCurrentModal = useSetCurrentModal();
  const { data } = useInformationSectionQuery({
    variables: {
      code: process.env.conferenceCode,
    },
  });
  const IllustrationComponent = getIllustration(illustration as Illustration);
  const deadlineDatetime =
    countdownToDeadline && Object.hasOwn(data.conference, countdownToDeadline)
      ? new Date(data.conference[countdownToDeadline].start)
      : null;
  const isModalCTA = cta?.link?.startsWith("modal:");
  const openModal = (e) => {
    if (!isModalCTA) {
      return;
    }
    e.preventDefault();

    const modalId = cta.link.replace("modal:", "") as ModalID;
    setCurrentModal(modalId);
  };

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
              <StyledHTMLText text={body} />
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
            <Button
              onClick={openModal}
              href={isModalCTA ? null : cta.link}
              variant="primary"
            >
              {cta.label}
            </Button>
          </>
        )}
        {IllustrationComponent && (
          <>
            <Spacer size="large" />
            <div className="max-w-[360px] lg:max-w-[488px] w-full">
              <IllustrationComponent className="w-full h-full mt-auto" />
            </div>
          </>
        )}
        {!IllustrationComponent && <Spacer size="3xl" />}
      </VerticalStack>
    </Section>
  );
};

InformationSection.dataFetching = (client) => {
  return [
    queryInformationSection(client, {
      code: process.env.conferenceCode,
    }),
  ];
};
