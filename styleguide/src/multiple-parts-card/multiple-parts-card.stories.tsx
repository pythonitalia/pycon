import React, { useState } from "react";
import { Text } from "../text";
import { MultiplePartsCard } from "./multiple-parts-card";
import { CardPart } from "./card-part";
import { Spacer } from "../spacer";
import { CardPartIncrements } from "./card-part-increments";
import { Heading } from "../heading";
import { CardPartOptions } from "./card-part-options";
import { differenceInCalendarDays } from "date-fns";
import { CardPartAddRemove } from "./card-part-addremove";
import { Tag } from "../tag";
import { CardPartTwoSides } from "./card-part-two-sides";

export default {
  title: "Multiple Parts Card",
};

export const Primary = () => (
  <div className="p-6">
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

      <CardPart background="red">
        <Text size={2}>red bg</Text>
      </CardPart>

      <CardPart background="blue">
        <Text size={2}>blue bg</Text>
      </CardPart>
    </MultiplePartsCard>
  </div>
);

export const CardWithContentAndOnePart = () => (
  <div className="p-6">
    <MultiplePartsCard
      cta={{
        link: "/test",
        label: "Request info",
      }}
    >
      <CardPart>
        <Heading size={3}>General info</Heading>
      </CardPart>
      <CardPart contentAlign="left" background="milk">
        <Text size={2}>
          We are here to help you! Let us know how we can do it
        </Text>
      </CardPart>
    </MultiplePartsCard>
  </div>
);

export const CardForProductItemIcons = () => (
  <div className="p-6">
    <MultiplePartsCard>
      <CardPart iconBackground="pink" icon="tickets" contentAlign="left">
        <Heading size={2}>Student</Heading>
      </CardPart>
      <CardPart contentAlign="left" background="milk">
        <Text size={2}>
          Lorem Ipsum is simply dummy text of the printing and typesetting
        </Text>
      </CardPart>
    </MultiplePartsCard>

    <Spacer size="large" />

    <MultiplePartsCard>
      <CardPart iconBackground="blue" icon="star" contentAlign="left">
        <Heading size={2}>Membership</Heading>
      </CardPart>
      <CardPart contentAlign="left" background="milk">
        <Text size={2}>
          Lorem Ipsum is simply dummy text of the printing and typesetting
        </Text>
      </CardPart>
    </MultiplePartsCard>
  </div>
);

export const WithIncrementExample = () => {
  const [counter1, setCounter1] = useState(0);
  const [counter2, setCounter2] = useState(0);
  const [counter3, setCounter3] = useState(0);
  const [counter4, setCounter4] = useState(0);

  return (
    <div className="p-6">
      <MultiplePartsCard>
        <CardPart iconBackground="yellow" icon="tshirt" contentAlign="left">
          <Heading size={2}>T-Shirt</Heading>
        </CardPart>
        <CardPart contentAlign="left" background="milk">
          <Text size={2}>
            Lorem Ipsum is simply dummy text of the printing and typesetting
          </Text>
        </CardPart>
        <CardPartIncrements
          onIncrement={() => setCounter1((value) => value + 1)}
          onDecrement={() => setCounter1((value) => value - 1)}
          value={counter1}
        >
          <div className="flex flex-col-reverse md:flex-row justify-center md:justify-start text-left md:gap-6">
            <Heading size={2}>€ 40</Heading>

            <Text size="label4" uppercase color="grey-500" weight="strong">
              Small
            </Text>
            {counter1 > 0 && <Text size="label3">€ 20 x2</Text>}
          </div>
        </CardPartIncrements>
        <CardPartIncrements
          onIncrement={() => setCounter2((value) => value + 1)}
          onDecrement={() => setCounter2((value) => value - 1)}
          value={counter2}
        >
          <Heading size={2}>€ 40</Heading>

          <Text size="label4" uppercase color="grey-500" weight="strong">
            Medium
          </Text>
          {counter2 > 0 && <Text size="label3">€ 20 x2</Text>}
        </CardPartIncrements>
        <CardPartIncrements
          onIncrement={() => setCounter3((value) => value + 1)}
          onDecrement={() => setCounter3((value) => value - 1)}
          value={counter3}
        >
          <Heading size={2}>€ 40</Heading>
          <Text size="label4" uppercase color="grey-500" weight="strong">
            Large
          </Text>
          {counter3 > 0 && <Text size="label3">€ 20 x2</Text>}
        </CardPartIncrements>
        <CardPartIncrements
          onIncrement={() => setCounter4((value) => value + 1)}
          onDecrement={() => setCounter4((value) => value - 1)}
          value={counter4}
        >
          <Heading size={2}>€ 40</Heading>
          <Text size="label4" uppercase color="grey-500" weight="strong">
            Extra Large
          </Text>
          {counter4 > 0 && <Text size="label3">€ 20 x2</Text>}
        </CardPartIncrements>
      </MultiplePartsCard>
    </div>
  );
};

export const MultiPartCardWithOptions = () => {
  const [temporaryRoom, setTemporaryRoom] = useState<any>({});
  const [storedRooms, setStoredRooms] = useState<any[]>([]);

  const nightsBetween = differenceInCalendarDays(
    new Date(temporaryRoom.checkout),
    new Date(temporaryRoom.checkin)
  );

  return (
    <div className="p-6">
      <MultiplePartsCard
        openByDefault={false}
        clickablePart="heading"
        expandTarget="content"
      >
        <CardPart
          iconBackground="green"
          icon="hotel"
          contentAlign="left"
          id="heading"
        >
          <Heading size={2}>Double Room</Heading>
        </CardPart>
        <CardPart id="content" contentAlign="left" background="milk">
          <Text size={2}>
            Lorem Ipsum is simply dummy text of the printing and typesetting
            <input type="text" placeholder="test" />
          </Text>
        </CardPart>

        {storedRooms.map((room, index) => {
          const nightsBetween = differenceInCalendarDays(
            new Date(room.checkout),
            new Date(room.checkin)
          );
          return (
            <CardPartOptions
              action="remove"
              onRemove={() => {
                const newRooms = [...storedRooms];
                newRooms.splice(index, 1);
                setStoredRooms(newRooms);
              }}
              options={[
                {
                  id: "checkin",
                  options: [
                    { label: "2022-10-10", value: "2022-10-10" },
                    { label: "2022-10-11", value: "2022-10-11" },
                    { label: "2022-10-12", value: "2022-10-12" },
                  ],
                  placeholder: "Check-in",
                  value: room.checkin,
                },
                {
                  id: "checkout",
                  options: [
                    { label: "2022-10-10", value: "2022-10-10" },
                    { label: "2022-10-11", value: "2022-10-11" },
                    { label: "2022-10-12", value: "2022-10-12" },
                  ],
                  placeholder: "Check-out",
                  value: room.checkout,
                },
                {
                  id: "beds",
                  options: [
                    { value: "double", label: "Double Bed" },
                    { value: "single", label: "2x Single Beds" },
                    { value: "another", label: "Very long single beds" },
                  ],
                  placeholder: "Bed layout",
                  value: room.beds,
                },
              ]}
            >
              <div>
                <Heading size={2}>
                  € {nightsBetween ? 40 * nightsBetween : 40}
                </Heading>
                <Text uppercase size="label3">
                  {nightsBetween ? `€ 40/night` : `/night`}
                </Text>
              </div>
            </CardPartOptions>
          );
        })}

        <CardPartOptions
          onConfirm={() => {
            setStoredRooms((rooms) => [...rooms, temporaryRoom]);
            setTemporaryRoom({});
          }}
          action="add"
          onChange={(id, e) => {
            if (id === "checkin") {
              setTemporaryRoom((room) => ({
                ...room,
                checkin: e.target.value,
              }));
            } else if (id === "checkout") {
              setTemporaryRoom((room) => ({
                ...room,
                checkout: e.target.value,
              }));
            } else if (id === "beds") {
              setTemporaryRoom((room) => ({
                ...room,
                beds: e.target.value,
              }));
            }
          }}
          options={[
            {
              id: "checkin",
              options: [
                { label: "2022-10-10", value: "2022-10-10" },
                { label: "2022-10-11", value: "2022-10-11" },
                { label: "2022-10-12", value: "2022-10-12" },
              ],
              placeholder: "Check-in",
              value: temporaryRoom.checkin,
            },
            {
              id: "checkout",
              options: [
                { label: "2022-10-10", value: "2022-10-10" },
                { label: "2022-10-11", value: "2022-10-11" },
                { label: "2022-10-12", value: "2022-10-12" },
              ],
              placeholder: "Check-out",
              value: temporaryRoom.checkout,
            },
            {
              id: "beds",
              options: [
                { value: "double", label: "Double + Single" },
                { value: "single", label: "3x Single Beds" },
                { value: "another", label: "Very long single beds" },
              ],
              placeholder: "Bed layout",
              value: temporaryRoom.beds,
            },
          ]}
        >
          <div className="flex items-end">
            <Heading size={2}>
              € {nightsBetween ? 40 * nightsBetween : 40}
            </Heading>
            <Text uppercase size="label3">
              {nightsBetween ? `€ 40/night` : `/night`}
            </Text>
          </div>
        </CardPartOptions>
      </MultiplePartsCard>
    </div>
  );
};

export const MultiPartCardWithVariableOptions = ({ numOfSelects }) => {
  const [temporaryRoom, setTemporaryRoom] = useState<any>({});
  const createObject = (index: number, longItem: boolean = false) => ({
    id: `obj-${index}`,
    options: [
      longItem
        ? { label: "1x Matrimoniale 2x Singoli", value: "2022-10-10" }
        : {
            label: "10 Giugno",
            value: "2022-10-10",
          },
      { label: "11 Giugno", value: "2022-10-11" },
      { label: "12 Giugno", value: "2022-10-12" },
    ],
    placeholder: `Object ${index}`,
    value: temporaryRoom[`obj-${index}`],
  });

  return (
    <div className="p-6">
      <MultiplePartsCard>
        <CardPart iconBackground="green" icon="hotel" contentAlign="left">
          <Heading size={2}>Double Room</Heading>
        </CardPart>
        <CardPart contentAlign="left" background="milk">
          <Text size={2}>
            Lorem Ipsum is simply dummy text of the printing and typesetting
          </Text>
        </CardPart>

        <CardPartOptions
          onConfirm={() => {
            setTemporaryRoom({});
          }}
          action="remove"
          onChange={(id, e) => {
            setTemporaryRoom((room) => ({
              ...room,
              [id]: e.target.value,
            }));
          }}
          options={new Array(numOfSelects)
            .fill(0)
            .map((_, index) => createObject(index, index === 2))}
        >
          <Heading size={2}>£350 3 x nights</Heading>
        </CardPartOptions>

        <CardPartOptions
          onConfirm={() => {
            setTemporaryRoom({});
          }}
          action="add"
          onChange={(id, e) => {
            setTemporaryRoom((room) => ({
              ...room,
              [id]: e.target.value,
            }));
          }}
          options={new Array(numOfSelects)
            .fill(0)
            .map((_, index) => createObject(index, index === 2))}
        >
          <Heading size={2}>Test Test Test</Heading>
        </CardPartOptions>
      </MultiplePartsCard>
    </div>
  );
};

MultiPartCardWithVariableOptions.argTypes = {
  numOfSelects: {
    defaultValue: 3,
    control: {
      type: "number",
    },
  },
};

export const AddRemoveCardPart = () => {
  const [added, setAdded] = useState(false);
  return (
    <div className="p-6">
      <MultiplePartsCard>
        <CardPart iconBackground="blue" icon="star" contentAlign="left">
          <Heading size={2}>Membership</Heading>
        </CardPart>

        <CardPart contentAlign="left" background="milk">
          <Text size={2}>
            Lorem Ipsum is simply dummy text of the printing and typesetting
          </Text>
        </CardPart>
        <CardPartAddRemove
          onAdd={() => setAdded(true)}
          onRemove={() => setAdded(false)}
          action={added ? "remove" : "add"}
        >
          <Heading size={2}>30£</Heading>
        </CardPartAddRemove>
      </MultiplePartsCard>
    </div>
  );
};

export const CardPartExpandable = () => {
  return (
    <div className="p-6">
      <MultiplePartsCard
        openByDefault={false}
        clickablePart="heading"
        expandTarget="content"
      >
        <CardPart
          iconBackground="blue"
          icon="star"
          contentAlign="left"
          id="heading"
          openLabel="Discover more"
        >
          <Heading size={2}>Membership [closed by default]</Heading>
        </CardPart>
        <CardPart id="content" contentAlign="left" background="milk">
          <Text size={2}>
            Lorem Ipsum is simply dummy text of the printing and typesetting
            Lorem Ipsum is simply dummy text of the printing and typesetting
            Lorem Ipsum is simply dummy text of the printing and typesetting
            Lorem Ipsum is simply dummy text of the printing and typesetting
            Lorem Ipsum is simply dummy text of the printing and typesetting
            Lorem Ipsum is simply dummy text of the printing and typesetting
            Lorem Ipsum is simply dummy text of the printing and typesetting
            Lorem Ipsum is simply dummy text of the printing and typesetting
          </Text>
        </CardPart>
        <CardPart>
          <Heading size={1}>€ 100</Heading>
          <Spacer size="xs" />
          <Text size={2}>flat price</Text>
        </CardPart>
      </MultiplePartsCard>
      <Spacer size="xl" />
      <MultiplePartsCard
        openByDefault={true}
        clickablePart="heading"
        expandTarget="content"
      >
        <CardPart
          iconBackground="blue"
          icon="star"
          contentAlign="left"
          id="heading"
          openLabel="Discover more"
        >
          <Heading size={2}>Membership [open by default]</Heading>
        </CardPart>
        <CardPart id="content" contentAlign="left" background="milk">
          <Text size={2}>
            Lorem Ipsum is simply dummy text of the printing and typesetting
            Lorem Ipsum is simply dummy text of the printing and typesetting
            Lorem Ipsum is simply dummy text of the printing and typesetting
            Lorem Ipsum is simply dummy text of the printing and typesetting
            Lorem Ipsum is simply dummy text of the printing and typesetting
            Lorem Ipsum is simply dummy text of the printing and typesetting
            Lorem Ipsum is simply dummy text of the printing and typesetting
            Lorem Ipsum is simply dummy text of the printing and typesetting
          </Text>
        </CardPart>
        <CardPart>
          <Heading size={1}>€ 100</Heading>
          <Spacer size="xs" />
          <Text size={2}>flat price</Text>
        </CardPart>
      </MultiplePartsCard>
    </div>
  );
};

export const CardPartTwoSidesExample = () => {
  return (
    <div className="p-6">
      <MultiplePartsCard>
        <CardPart contentAlign="left">
          <Heading size={2}>Example with tag</Heading>
        </CardPart>
        <CardPartTwoSides rightSide={<Tag color="red">Sold-out</Tag>}>
          <Heading size={2}>£400</Heading>
        </CardPartTwoSides>
      </MultiplePartsCard>
      <Spacer size="small" />
      <MultiplePartsCard>
        <CardPart contentAlign="left">
          <Heading size={2}>Different color & length</Heading>
        </CardPart>
        <CardPartTwoSides rightSide={<Tag color="success">Buy me now!</Tag>}>
          <Heading size={2}>$250</Heading>
        </CardPartTwoSides>
      </MultiplePartsCard>
    </div>
  );
};

export const CardWithInputsInItAndFocus = () => {
  return (
    <div className="p-6">
      <input type="text" placeholder="Outside input" />

      <MultiplePartsCard
        openByDefault={false}
        clickablePart="heading"
        expandTarget="content"
      >
        <CardPart
          iconBackground="blue"
          icon="star"
          contentAlign="left"
          id="heading"
          openLabel="Discover more"
        >
          <Heading size={2}>Membership</Heading>
        </CardPart>
        <CardPart id="content" contentAlign="left" background="milk">
          <Text size={2}>
            <input type="text" placeholder="Enter your name" />
            <input type="email" placeholder="Enter your email" />
          </Text>
        </CardPart>
        <CardPart>
          <Heading size={1}>€ 100</Heading>
          <Spacer size="xs" />
          <Text size={2}>flat price</Text>
        </CardPart>
      </MultiplePartsCard>
    </div>
  );
};

export const CardPartIconsWithIcons = ({ size }) => {
  return (
    <div className="p-6">
      <MultiplePartsCard>
        <CardPart
          size={size}
          rightSideIcon="arrow"
          rightSideIconBackground="none"
          rightSideIconSize="small"
          contentAlign="left"
          openLabel="Discover more"
        >
          <Text size="label3">Icon on the right only</Text>
        </CardPart>
      </MultiplePartsCard>
      <Spacer size="large" />
      <MultiplePartsCard>
        <CardPart
          size={size}
          icon="arrow"
          iconBackground="none"
          iconSize="small"
          contentAlign="left"
          openLabel="Discover more"
        >
          <Text size="label3">Icon on the left only</Text>
        </CardPart>
      </MultiplePartsCard>
      <Spacer size="large" />
      <MultiplePartsCard>
        <CardPart
          size={size}
          icon="arrow"
          iconBackground="none"
          iconSize="small"
          rightSideIcon="arrow"
          rightSideIconBackground="none"
          rightSideIconSize="small"
          contentAlign="left"
          openLabel="Discover more"
        >
          <Text size="label3">Icon on both sides</Text>
        </CardPart>
      </MultiplePartsCard>
    </div>
  );
};

CardPartIconsWithIcons.argTypes = {
  size: {
    control: {
      type: "select",
      options: ["small", "large"],
    },
  },
};

export const CarPartWithHoveColor = () => (
  <div>
    <MultiplePartsCard>
      <CardPart contentAlign="left" id="heading" hoverColor="green">
        <Heading size={2}>Student</Heading>
      </CardPart>
    </MultiplePartsCard>
    <MultiplePartsCard>
      <CardPart contentAlign="left" id="heading" hoverColor="green">
        <Heading size={2}>Student</Heading>
      </CardPart>
    </MultiplePartsCard>
  </div>
);
