import { getApolloClient } from "~/apollo/sc-client";
import { Cta, querySchedulePreviewSection } from "~/types";

import { SchedulePreviewSectionComponent } from "./client";

type Props = {
  title: string;
  primaryCta: Cta | null;
  secondaryCta: Cta | null;
};

export const SchedulePreviewSection = async ({
  title,
  primaryCta,
  secondaryCta,
}: Props) => {
  const language = "en";
  // const language = useCurrentLanguage();
  const client = getApolloClient();
  const {
    data: { conference },
  } = await querySchedulePreviewSection(client, {
    code: process.env.conferenceCode,
  });

  const days = conference.days;

  return (
    <SchedulePreviewSectionComponent
      days={days}
      title={title}
      primaryCta={primaryCta}
      secondaryCta={secondaryCta}
    />
  );
};
