import {
  Button,
  CardPart,
  Container,
  Heading,
  MultiplePartsCard,
  Section,
  Spacer,
  StyledHTMLText,
} from "@python-italia/pycon-styleguide";

import { BodyTextSize, type TextSection as TextSectionType } from "~/types";

import { Fragment } from "react";
import { type ModalID, useSetCurrentModal } from "../modal/context";

export const TextSection = ({
  title,
  isMainTitle,
  subtitle,
  body,
  bodyTextSize,
  illustration,
  accordions,
  cta,
}: TextSectionType) => {
  const setCurrentModal = useSetCurrentModal();
  const onlyAccordions = !title && !subtitle && !body && !cta;
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
      spacingSize={isMainTitle ? "2xl" : "xl"}
      illustration={(illustration as any) || undefined}
    >
      <Container noPadding center={false} size="medium">
        {title && (
          <>
            <Heading size={isMainTitle ? "display1" : "display2"}>
              {title}
            </Heading>
            {(subtitle || body || cta) && <Spacer size="xl" />}
          </>
        )}

        {subtitle && (
          <>
            <Heading size={2}>{subtitle}</Heading>
            {(body || cta) && <Spacer size="medium" />}
          </>
        )}
        {body && (
          <>
            <StyledHTMLText
              text={body}
              baseTextSize={bodyTextSize === BodyTextSize.Text_1 ? 1 : 2}
            />
            {cta && <Spacer size="large" />}
          </>
        )}
        {cta && (
          <Button
            variant="secondary"
            onClick={openModal}
            href={isModalCTA ? null : cta.link}
            fullWidth="mobile"
          >
            {cta.label}
          </Button>
        )}
      </Container>
      <Container noPadding size="2md">
        {accordions.length > 0 && (
          <>
            {!onlyAccordions && <Spacer size="xl" />}
            {accordions?.map((accordion, index) => (
              <Fragment key={index}>
                <MultiplePartsCard
                  clickablePart="heading"
                  expandTarget="content"
                  openByDefault={accordion.isOpen}
                >
                  <CardPart contentAlign="left" id="heading">
                    <Heading size={3}>{accordion.title}</Heading>
                  </CardPart>
                  <CardPart id="content" contentAlign="left" background="milk">
                    <StyledHTMLText text={accordion.body} baseTextSize={2} />
                  </CardPart>
                </MultiplePartsCard>
                {/* todo replace with MultiplePartsCardCollection */}
                {index !== accordions.length - 1 && <Spacer size="small" />}
              </Fragment>
            ))}
          </>
        )}
      </Container>
    </Section>
  );
};
