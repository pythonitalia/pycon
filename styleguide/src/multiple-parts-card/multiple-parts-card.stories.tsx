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
      <CardPart title="Student">
        <Text size={2}>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        </Text>
      </CardPart>

      <CardPart title="€ 100" titleSize="large">
        <Text size={2}>flat price</Text>
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
      <CardPart title="General info" titleSize="small" />
      <CardPart contentAlign="left" noBg>
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
      <CardPart
        iconBackground="pink"
        title="Student"
        icon="ticket"
        contentAlign="left"
      />
      <CardPart contentAlign="left" noBg>
        <Text size={2}>
          Lorem Ipsum is simply dummy text of the printing and typesetting
        </Text>
      </CardPart>
    </MultiplePartsCard>

    <Spacer size="large" />

    <MultiplePartsCard>
      <CardPart
        iconBackground="blue"
        title="Membership"
        icon="star"
        contentAlign="left"
      />
      <CardPart contentAlign="left" noBg>
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
        <CardPart
          iconBackground="yellow"
          title="T-Shirt"
          icon="tshirt"
          contentAlign="left"
        />
        <CardPart contentAlign="left" noBg>
          <Text size={2}>
            Lorem Ipsum is simply dummy text of the printing and typesetting
          </Text>
        </CardPart>
        <CardPartIncrements
          onIncrement={() => setCounter1((value) => value + 1)}
          onDecrement={() => setCounter1((value) => value - 1)}
          value={counter1}
        >
          <Text size="label1">Small</Text>
          <Heading size={2}>€ 40</Heading>
          {counter1 > 0 && <Text size="label3">€ 20 x2</Text>}
        </CardPartIncrements>
        <CardPartIncrements
          onIncrement={() => setCounter2((value) => value + 1)}
          onDecrement={() => setCounter2((value) => value - 1)}
          value={counter2}
        >
          <Text size="label1">Medium</Text>
          <Heading size={2}>€ 40</Heading>
          {counter2 > 0 && <Text size="label3">€ 20 x2</Text>}
        </CardPartIncrements>
        <CardPartIncrements
          onIncrement={() => setCounter3((value) => value + 1)}
          onDecrement={() => setCounter3((value) => value - 1)}
          value={counter3}
        >
          <Text size="label1">Large</Text>
          <Heading size={2}>€ 40</Heading>
          {counter3 > 0 && <Text size="label3">€ 20 x2</Text>}
        </CardPartIncrements>
        <CardPartIncrements
          onIncrement={() => setCounter4((value) => value + 1)}
          onDecrement={() => setCounter4((value) => value - 1)}
          value={counter4}
        >
          <Text size="label1">Extra Large</Text>
          <Heading size={2}>€ 40</Heading>
          {counter4 > 0 && <Text size="label3">€ 20 x2</Text>}
        </CardPartIncrements>
      </MultiplePartsCard>
    </div>
  );
};

export const MultiPartCardWithOptions = () => {
  const [temporaryRoom, setTemporaryRoom] = useState({});
  const [storedRooms, setStoredRooms] = useState([]);

  const nightsBetween = differenceInCalendarDays(
    new Date(temporaryRoom.checkout),
    new Date(temporaryRoom.checkin)
  );
  console.log("nightsBetween", nightsBetween);

  return (
    <div className="p-6">
      <MultiplePartsCard>
        <CardPart
          iconBackground="green"
          title="Double Room"
          icon="hotel"
          contentAlign="left"
        />
        <CardPart contentAlign="left" noBg>
          <Text size={2}>
            Lorem Ipsum is simply dummy text of the printing and typesetting
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
              selects={[
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
                  ],
                  placeholder: "Bed layout",
                  value: room.beds,
                },
              ]}
            >
              <Heading size={2}>
                € {nightsBetween ? 40 * nightsBetween : 40}
              </Heading>
              <Text uppercase size="label3">
                {nightsBetween ? `€ 40/night` : `/night`}
              </Text>
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
          selects={[
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
              ],
              placeholder: "Bed layout",
              value: temporaryRoom.beds,
            },
          ]}
        >
          <Heading size={2}>
            € {nightsBetween ? 40 * nightsBetween : 40}
          </Heading>
          <Text uppercase size="label3">
            {nightsBetween ? `€ 40/night` : `/night`}
          </Text>
        </CardPartOptions>
      </MultiplePartsCard>
    </div>
  );
};

export const AddRemoveCardPart = () => {
  const [added, setAdded] = useState(false);
  return (
    <div className="p-6">
      <MultiplePartsCard>
        <CardPart
          iconBackground="blue"
          title="Membership"
          icon="star"
          contentAlign="left"
        />
        <CardPart contentAlign="left" noBg>
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

export const CardPartExpandable = ({ expanded }) => {
  return (
    <div className="p-6">
      <MultiplePartsCard
        openByDefault={false}
        clickablePart="heading"
        expandTarget="content"
      >
        <CardPart
          iconBackground="blue"
          title="Membership"
          icon="star"
          contentAlign="left"
          id="heading"
          openLabel="Discover more"
        />
        <CardPart id="content" contentAlign="left" noBg>
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
        <CardPart title="€ 100" titleSize="large">
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
          title="Membership"
          icon="star"
          contentAlign="left"
          id="heading"
          openLabel="Discover more"
        />
        <CardPart id="content" contentAlign="left" noBg>
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
        <CardPart title="€ 100" titleSize="large">
          <Text size={2}>flat price</Text>
        </CardPart>
      </MultiplePartsCard>
    </div>
  );
};

CardPartExpandable.argTypes = {
  expanded: {
    defaultValue: false,
    control: {
      type: "boolean",
    },
  },
};
