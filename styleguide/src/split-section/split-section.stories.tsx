import React from "react";
import { Button } from "../button";
import { Countdown } from "../countdown";
import { Heading } from "../heading";
import {
  Cathedral,
  Snake1,
  Snake4,
  Snake5,
  SnakePencil,
} from "../illustrations";
import { Florence2 } from "../illustrations/florence2";
import { Page } from "../page/index";
import { Spacer } from "../spacer";
import { Text } from "../text";
import { SplitSection } from "./split-section";

export const Standard = ({ ...props }) => (
  <div className="py-4">
    <SplitSection
      sideContent={<Florence2 />}
      sideContentBackground={Florence2.backgroundColor}
      {...props}
    >
      <Heading size="display2">Become a sponsor</Heading>
      <Spacer size="medium" />
      <Text size={1}>
        Sponsoring PyConIT guarantees you strongly targeted visibility towards
        senior developers and software engineers.
      </Text>
      <Spacer size="large" />
      <Button onClick={() => {}} variant="secondary">
        Become a sponsor
      </Button>
    </SplitSection>
  </div>
);

export const WithCustomIllustration = () => (
  <div className="py-4">
    <SplitSection
      sideContent={<SnakePencil />}
      sideContentType="other"
      sideContentPadding={false}
      contentSpacing="medium"
      hideSideContentOnMobile={true}
    >
      <Heading size="display2">Become a sponsor</Heading>
      <Spacer size="medium" />
      <Text size={1}>
        Sponsoring PyConIT guarantees you strongly targeted visibility towards
        senior developers and software engineers.
      </Text>
      <Spacer size="large" />
      <Button onClick={() => {}} variant="secondary">
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
      contentSpacing="medium"
    >
      <Heading size="display2">Call for proposals [inverted]</Heading>
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
      sideContentType="other"
      hideSideContentOnMobile
      contentSpacing="medium"
    >
      <Heading size="display2">Not inverted</Heading>
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
      <Button onClick={() => {}} variant="primary">
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
      >
        <Heading size="display2">Become a sponsor</Heading>
        <Spacer size="medium" />
        <Text size={1}>
          Sponsoring PyConIT guarantees you strongly targeted visibility towards
          senior developers and software engineers.
        </Text>
        <Spacer size="large" />
        <Button onClick={() => {}} variant="secondary">
          Become a sponsor
        </Button>
      </SplitSection>
      <SplitSection
        sideContent={<Cathedral />}
        sideContentBackground={Cathedral.backgroundColor}
      >
        <Heading size="display2">Buy a ticket</Heading>
        <Spacer size="medium" />
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
        contentSpacing="medium"
      >
        <Heading size="display2">Call for proposals</Heading>
        <Spacer size="medium" />
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
        invert
        sideContent={<Snake4 />}
        sideContentBackground={Snake4.backgroundColor}
      >
        <Heading size="display2">Keynoters here</Heading>
        <Spacer size="medium" />
        <Text size={1}>Some more text</Text>
        <Spacer size="large" />
        <Button onClick={() => {}} variant="primary">
          Hello look at me! I am a text!
        </Button>
      </SplitSection>
      <SplitSection
        sideContent={<Snake5 />}
        sideContentBackground={Snake5.backgroundColor}
      >
        <Heading size="display2">Spacing tests</Heading>
        <Spacer size="medium" />
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
      <SplitSection
        invert
        sideContent={<Snake1 />}
        sideContentBackground={Snake1.backgroundColor}
      >
        <Heading size="display2">Inverted spacing tests</Heading>
        <Spacer size="medium" />

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
