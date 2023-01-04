import {
  CardPart,
  GridSection,
  Heading,
  Link,
  MultiplePartsCard,
  Page,
  Section,
} from "@python-italia/pycon-styleguide";
import React from "react";

type Action = {
  link: string;
  label: React.ReactNode;
  icon: Parameters<typeof CardPart>[0]["icon"];
  iconBackground: Parameters<typeof CardPart>[0]["iconBackground"];
};

export const ProfilePageHandler = () => {
  const availableActions: Action[] = [
    {
      link: "/profile/view",
      label: "My Profile",
      icon: "star",
      iconBackground: "blue",
    },
    {
      link: "/profile/my-tickets",
      label: "My Tickets",
      icon: "ticket",
      iconBackground: "pink",
    },
    {
      link: "/profile/my-proposals",
      label: "My Proposals",
      icon: "ticket",
      iconBackground: "pink",
    },
  ];
  return (
    <Page endSeparator={false}>
      <Section background="coral">
        <Heading size="display2">Hello Marco!</Heading>
      </Section>
      <GridSection cols={2}>
        {availableActions.map((action) => (
          <Link hoverColor="black" href={action.link}>
            <MultiplePartsCard>
              <CardPart
                icon={action.icon}
                iconBackground={action.iconBackground}
                rightSideIcon="arrow"
              >
                <Heading size={3}>{action.label}</Heading>
              </CardPart>
            </MultiplePartsCard>
          </Link>
        ))}
      </GridSection>
    </Page>
  );
};
