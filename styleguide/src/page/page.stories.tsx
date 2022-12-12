import React from "react";
import { SplitSection } from "../split-section/split-section";
import { Logo } from "../logo/logo";
import { NavBar } from "../navbar/navbar";
import { Cathedral, Snake5 } from "../illustrations";
import { Text } from "../text";
import { Spacer } from "../spacer";
import { Button } from "../button";
import { SectionsWrapper } from "../sections-wrapper";
import { Heading } from "../heading";
import { SnakeCountdown } from "../snake-countdown";
import { Section } from "../section";

export default {
  title: "Page examples",
};

export const Standard = () => (
  <div>
    <NavBar
      actions={[
        {
          text: "Buy Tickets",
          icon: "tickets",
          link: "/tickets",
        },
        {
          text: "Dashboard",
          icon: "user",
        },
      ]}
      mainLinks={[
        {
          text: "Live",
          link: "/live",
        },
        {
          text: "Agenda",
          link: "/schedule",
        },
        {
          text: "Speakers",
          link: "/speakers",
        },
        {
          text: "Where",
          link: "/where",
        },
        {
          text: "Keynotes",
          link: "/keynotes",
        },
        {
          text: "Tickets",
          link: "/tickets",
        },
      ]}
      secondaryLinks={new Array(15)
        .fill({
          text: "Beginners Day",
          link: "/beginners-day",
        })
        .map((l, index) => ({
          ...l,
          text: `${l.text} ${index}`,
        }))}
      logo={Logo}
      mobileLogo={Logo}
      bottomBarLink={{
        link: "/it",
        text: "Switch to Italian",
      }}
    />
    <SectionsWrapper>
      <Section>
        <Heading size="display1">
          Welcome to the Python Italia Conference
        </Heading>
      </Section>
      <SplitSection
        sideContent={<Cathedral />}
        sideContentBackground={Cathedral.backgroundColor}
        title="Buy a ticket"
      >
        <Text size={1}>We have tickets</Text>
        <Spacer size="large" />
        <Button onClick={() => {}} role="primary">
          Buy ticket
        </Button>
      </SplitSection>
      <SplitSection
        sideContent={
          <SnakeCountdown
            snakeLookingAt="right"
            deadline={new Date(2023, 2, 10, 10, 0, 0)}
          />
        }
        invert
        sideContentType="other"
        hideSideContentOnMobile
        spacing="larger-content"
        title="Call for proposals [inverted]"
      >
        <Spacer size="medium" />
        <Heading size={2}>PyCon Italia is looking for you!</Heading>
        <Spacer size="medium" />
        <SnakeCountdown
          deadline={new Date(2023, 2, 10, 10, 0, 0)}
          className="lg:hidden"
        />
        <Spacer size="medium" />
        <Text size={1}>
          PyCon Italia is seeking speakers of all experience levels and
          backgrounds to contribute to our conference program! If you use Python
          professionally, as a hobbyist or are just excited about Python or
          programming and open source communities, we would love to hear from
          you.
        </Text>
        <Spacer size="large" />
        <Button onClick={() => {}} role="primary">
          Buy ticket
        </Button>
      </SplitSection>
      <SplitSection
        sideContent={<Snake5 />}
        sideContentBackground={Snake5.backgroundColor}
        title="Spacing tests"
      >
        <Spacer size="medium" />
        <Heading size={2}>PyCon Italia is looking for you!</Heading>
        <Spacer size="medium" />
        <Text size={1}>
          PyCon Italia is seeking speakers of all experience levels and
          backgrounds to contribute to our conference program! If you use Python
          professionally, as a hobbyist or are just excited about Python or
          programming and open source communities, we would love to hear from
          you.
        </Text>
        <Spacer size="large" />
        <Button onClick={() => {}} role="secondary">
          Submit now
        </Button>
      </SplitSection>
    </SectionsWrapper>
  </div>
);
