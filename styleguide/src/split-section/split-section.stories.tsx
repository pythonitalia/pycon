import React from "react";
import { Cathedral, Snake4, Snake5, Snake1 } from "../illustrations";
import { SplitSection } from "./split-section";
import { Text } from "../text";
import { Spacer } from "../spacer";
import { Button } from "../button";
import { Florence2 } from "../illustrations/florence2";
import { Page } from "../page/index";
import { Heading } from "../heading";
import { Countdown } from "../countdown";

export const Standard = ({ ...props }) => (
  <div className="py-4">
    <SplitSection
      sideContent={<Florence2 />}
      sideContentBackground={Florence2.backgroundColor}
      title="Become a sponsor"
      {...props}
    >
      <Text size={1}>
        Sponsoring PyConIT guarantees you strongly targeted visibility towards
        senior developers and software engineers.
      </Text>
      <Spacer size="large" />
      <Button onClick={() => {}} role="secondary">
        Become a sponsor
      </Button>
    </SplitSection>
  </div>
);

export const WithOtherSideContent = ({ ...props }) => (
  <div className="py-4">
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
        programming and open source communities, we would love to hear from you.
      </Text>
      <Spacer size="large" />
      <Button onClick={() => {}} role="primary">
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
      sideContentType="other"
      hideSideContentOnMobile
      spacing="larger-content"
      title="Not inverted"
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
        programming and open source communities, we would love to hear from you.
      </Text>
      <Spacer size="large" />
      <Button onClick={() => {}} role="primary">
        Buy ticket
      </Button>
    </SplitSection>
  </div>
);

export const MultipleSections = ({ ...props }) => (
  <div className="py-4">
    <Page>
      <SplitSection
        sideContent={<Florence2 />}
        sideContentBackground={Florence2.backgroundColor}
        title="Become a sponsor"
      >
        <Text size={1}>
          Sponsoring PyConIT guarantees you strongly targeted visibility towards
          senior developers and software engineers.
        </Text>
        <Spacer size="large" />
        <Button onClick={() => {}} role="secondary">
          Become a sponsor
        </Button>
      </SplitSection>
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
          <Countdown
            snakeLookingAt="right"
            deadline={new Date(2023, 2, 10, 10, 0, 0)}
          />
        }
        invert
        sideContentType="other"
        hideSideContentOnMobile
        spacing="larger-content"
        title="Call for proposals"
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
        <Button onClick={() => {}} role="primary">
          Buy ticket
        </Button>
      </SplitSection>
      <SplitSection
        invert
        sideContent={<Snake4 />}
        sideContentBackground={Snake4.backgroundColor}
        title="Keynoters here"
      >
        <Text size={1}>Some more text</Text>
        <Spacer size="large" />
        <Button onClick={() => {}} role="primary">
          Hello look at me! I am a text!
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
      <SplitSection
        invert
        sideContent={<Snake1 />}
        sideContentBackground={Snake1.backgroundColor}
        title="Inverted Spacing tests"
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
    </Page>
  </div>
);

export default {
  title: "SplitSection",
  component: Standard,
  argTypes: {
    invert: {
      control: {
        type: "boolean",
      },
    },
  },
};
