import React from "react";
import { Button } from "../button";
import { Countdown } from "../countdown";
import { Heading } from "../heading";
import { Cathedral, Snake5 } from "../illustrations";
import { Logo } from "../logo/logo";
import { CardPart, MultiplePartsCard } from "../multiple-parts-card";
import { NavBar } from "../navbar/navbar";
import { Section } from "../section";
import { SliderGrid } from "../slider-grid";
import { Spacer } from "../spacer";
import { SplitSection } from "../split-section/split-section";
import { Text } from "../text";
import { Page } from "./page";

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
    <Page>
      <Section>
        <Heading size="display1">
          Welcome to the Python Italia Conference
        </Heading>
      </Section>
      <SliderGrid background="snake" cols={3}>
        <MultiplePartsCard
          cta={{
            link: "/test",
            label: "Buy tickets",
          }}
        >
          <CardPart>
            <Heading size={2}>Student</Heading>
            <Spacer size="xs" />
            <Text size={2}>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            </Text>
          </CardPart>

          <CardPart>
            <Heading size={1}>€ 100</Heading>
            <Spacer size="xs" />
            <Text size={2}>flat price</Text>
          </CardPart>
        </MultiplePartsCard>

        <MultiplePartsCard
          cta={{
            link: "/test",
            label: "Buy tickets",
          }}
        >
          <CardPart>
            <Heading size={2}>Regular</Heading>
            <Spacer size="xs" />
            <Text size={2}>
              Buying now your ticket, you can save up to the 30%
            </Text>
          </CardPart>

          <CardPart>
            <Heading size={1}>€ 180</Heading>
            <Spacer size="xs" />
            <Text size={2}>Early bird</Text>
          </CardPart>
        </MultiplePartsCard>

        <MultiplePartsCard
          cta={{
            link: "/test",
            label: "Buy tickets",
          }}
        >
          <CardPart>
            <Heading size={2}>Business</Heading>
            <Spacer size="xs" />
            <Text size={2}>
              Buying now your ticket, you can save up to the 25%
            </Text>
          </CardPart>

          <CardPart>
            <Heading size={1}>€ 250</Heading>
            <Spacer size="xs" />
            <Text size={2}>Early bird</Text>
          </CardPart>
        </MultiplePartsCard>
      </SliderGrid>

      <SplitSection
        sideContent={<Cathedral />}
        sideContentBackground={Cathedral.backgroundColor}
        title="Buy a ticket"
      >
        <Text size={1}>We have tickets</Text>
        <Spacer size="large" />
        <Button onClick={() => {}} variant="primary">
          Buy ticket
        </Button>
      </SplitSection>
      <SplitSection
        sideContent={
          <Countdown
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
        <Countdown
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
        <Button onClick={() => {}} variant="primary">
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
        <Button onClick={() => {}} variant="secondary">
          Submit now
        </Button>
      </SplitSection>
    </Page>
  </div>
);
