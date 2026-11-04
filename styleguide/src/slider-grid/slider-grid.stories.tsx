import React from "react";
import { MultiplePartsCard, CardPart } from "../multiple-parts-card";
import { SliderGrid } from "./slider-grid";
import { Text } from "../text";
import { Heading } from "../heading";
import { Spacer } from "../spacer";
import { SpeakerCard } from "../speaker-card";
import { Link } from "../link";

export const Default = () => {
  return (
    <div className="py-12">
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
            <Text size={2}>Lorem ipsum dolor sit amet</Text>
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
    </div>
  );
};

export const DynamicCards = ({ cols, items }) => {
  return (
    <div className="py-12">
      <SliderGrid background="snake" cols={cols}>
        {Array(items)
          .fill(0)
          .map((_, index) => (
            <MultiplePartsCard
              key={index}
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
          ))}
      </SliderGrid>
    </div>
  );
};
DynamicCards.argTypes = {
  cols: {
    defaultValue: 2,
    control: {
      type: "number",
    },
  },
  items: {
    defaultValue: 2,
    control: {
      type: "number",
    },
  },
};

export const SpeakerCardGrid = () => {
  return (
    <SliderGrid cols={3} mdCols={2}>
      <Link href="/" noHover>
        <SpeakerCard
          speakerName="John Doe"
          talkTitle="Clickable"
          portraitUrl="https://images.unsplash.com/photo-1508991170629-9f4cbd6bd8a6?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=900&ixid=MnwxfDB8MXxyYW5kb218MHx8ZmFjZSx3b21hbix5b3VuZ3x8fHx8fDE2NzUwMjY4NjU&ixlib=rb-4.0.3&q=80&w=900"
        />
      </Link>
      <SpeakerCard
        speakerName="Jane Doe"
        talkTitle="Long talk title that will cause multiple lines"
        portraitUrl="https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=900&ixid=MnwxfDB8MXxyYW5kb218MHx8ZmFjZSx3b21hbix5b3VuZ3x8fHx8fDE2NzUwMzAzMzY&ixlib=rb-4.0.3&q=80&w=900"
      />
      <SpeakerCard
        speakerName="Jane Doe"
        talkTitle="Short"
        portraitUrl="https://images.unsplash.com/flagged/photo-1559502867-c406bd78ff24?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=900&ixid=MnwxfDB8MXxyYW5kb218MHx8ZmFjZSx3b21hbix5b3VuZ3x8fHx8fDE2NzUwMjY5MzM&ixlib=rb-4.0.3&q=80&w=900"
      />
      <SpeakerCard
        speakerName="Jane Doe"
        talkTitle="Longer talk title that will cause multiple lines longer to 3 lines?"
        portraitUrl="https://images.unsplash.com/photo-1519336555923-59661f41bb45?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=900&ixid=MnwxfDB8MXxyYW5kb218MHx8ZmFjZSx3b21hbix5b3VuZ3x8fHx8fDE2NzUwMjY5NDU&ixlib=rb-4.0.3&q=80&w=900"
      />

      <SpeakerCard
        speakerName="Jane Doe"
        talkTitle="Doing things"
        portraitUrl="https://images.unsplash.com/photo-1512310604669-443f26c35f52?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=900&ixid=MnwxfDB8MXxyYW5kb218MHx8ZmFjZSx3b21hbix5b3VuZ3x8fHx8fDE2NzUwMjY5NTY&ixlib=rb-4.0.3&q=80&w=900"
      />

      <SpeakerCard
        speakerName="Jane Doe"
        talkTitle="Doing things"
        portraitUrl="https://images.unsplash.com/photo-1492106087820-71f1a00d2b11?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=900&ixid=MnwxfDB8MXxyYW5kb218MHx8ZmFjZSx3b21hbix5b3VuZ3x8fHx8fDE2NzUwMjY5ODE&ixlib=rb-4.0.3&q=80&w=900"
      />

      <SpeakerCard
        speakerName="Jane Doe"
        talkTitle="Doing things"
        portraitUrl="https://images.unsplash.com/photo-1528684394826-ea798614d051?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=900&ixid=MnwxfDB8MXxyYW5kb218MHx8ZmFjZSx3b21hbix5b3VuZ3x8fHx8fDE2NzUwMzAzMTg&ixlib=rb-4.0.3&q=80&w=900"
      />

      <SpeakerCard
        speakerName="Jane Doe"
        talkTitle="Doing things"
        portraitUrl="https://images.unsplash.com/photo-1534528741775-53994a69daeb?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=900&ixid=MnwxfDB8MXxyYW5kb218MHx8ZmFjZSx3b21hbix5b3VuZ3x8fHx8fDE2NzUwMzQ1NDE&ixlib=rb-4.0.3&q=80&w=900"
      />

      <SpeakerCard
        speakerName="Jane Doe"
        talkTitle="Doing things"
        portraitUrl="https://images.unsplash.com/photo-1479936343636-73cdc5aae0c3?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=900&ixid=MnwxfDB8MXxyYW5kb218MHx8ZmFjZSx3b21hbix5b3VuZ3x8fHx8fDE2NzUwMzA1MTY&ixlib=rb-4.0.3&q=80&w=900"
      />
      <SpeakerCard
        speakerName="Jane Doe"
        talkTitle="Doing things"
        portraitUrl="https://images.unsplash.com/photo-1476101751557-bbe4d57684e9?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=900&ixid=MnwxfDB8MXxyYW5kb218MHx8ZmFjZSx3b21hbix5b3VuZ3x8fHx8fDE2NzUwMzA2MTU&ixlib=rb-4.0.3&q=80&w=900"
      />
    </SliderGrid>
  );
};

export const SingleItem = () => {
  return (
    <SliderGrid cols={3} mdCols={2}>
      <SpeakerCard
        speakerName="John Doe"
        talkTitle="Clickable"
        portraitUrl="https://images.unsplash.com/photo-1508991170629-9f4cbd6bd8a6?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=900&ixid=MnwxfDB8MXxyYW5kb218MHx8ZmFjZSx3b21hbix5b3VuZ3x8fHx8fDE2NzUwMjY4NjU&ixlib=rb-4.0.3&q=80&w=900"
      />
    </SliderGrid>
  );
};

export default {
  title: "Slider Grid",
  component: Default,
};
