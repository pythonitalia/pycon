import {
  Heading,
  StyledHTMLText,
  Spacer,
  Section,
  Container,
} from "@python-italia/pycon-styleguide";

import { TextSection as TextSectionType } from "~/types";

export const SponsorLeadSection = ({ title, body }: TextSectionType) => {
  console.log({ title, body });
  return (
    <Section spacingSize={"xl"}>
      <Container noPadding center={false} size="medium">
        <Heading size={2}>{title}</Heading>
        <Spacer size="xl" />

        <StyledHTMLText text={body} baseTextSize={1} />
      </Container>
    </Section>
  );
};
