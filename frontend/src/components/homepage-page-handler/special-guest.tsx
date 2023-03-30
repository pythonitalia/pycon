import {
  Button,
  Grid,
  GridColumn,
  Heading,
  Section,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import {
  SnakeInDragon,
  SnakeInDragonInverted,
} from "@python-italia/pycon-styleguide/illustrations";
import React from "react";
import { FormattedMessage } from "react-intl";

import { useCurrentLanguage } from "~/locale/context";

import { createHref } from "../link";
import bg from "./background.svg";
import specialGuestPhoto from "./special-guest-photo.jpg";

export const SpecialGuest = () => {
  const language = useCurrentLanguage();
  return (
    <div
      className="relative bg-[#151C28] overflow-hidden"
      style={{
        height: bg.height,
      }}
    >
      <Section spacingSize="3xl">
        <div
          style={{
            backgroundImage: `url("${bg.src}")`,
          }}
          className="h-screen w-full absolute top-0 z-1 pointer-events-none"
        />
        <Grid cols={12}>
          <GridColumn colSpan={7}>
            <Heading size="display2" color="milk">
              <FormattedMessage id="specialGuest.title" />
            </Heading>
            <Spacer size="xl" showOnlyOn="desktop" />
            <Spacer size="medium" showOnlyOn="mobile" />
            <Spacer size="medium" showOnlyOn="tablet" />
            <div className="hidden lg:block">
              <SnakeInDragon />
            </div>
            <div className="lg:hidden flex items-end justify-end">
              <SnakeInDragonInverted />
            </div>
          </GridColumn>
          <GridColumn
            colSpan={4}
            className="flex flex-col items-center justify-center z-10"
          >
            <Spacer size="medium" showOnlyOn="mobile" />
            <Spacer size="medium" showOnlyOn="tablet" />
            <img
              src={specialGuestPhoto.src}
              className="w-72 aspect-square object-cover border"
            />
            <Spacer size="medium" />
            <Heading size={1} color="milk" align="center">
              Samantha Cristoforetti
            </Heading>
            <Heading size={3} align="center" color="milk">
              ESA Astronaut
            </Heading>
            <Spacer size="medium" />
            <Text size="label1" color="coral">
              <FormattedMessage id="specialGuest.date" />
            </Text>
            <Spacer size="medium" />
            <Button
              href={createHref({
                path: "/event/qa-with-esa-astronaut-samantha-cristoforetti",
                locale: language,
              })}
              role="secondary"
            >
              <FormattedMessage id="jobboard.discoverMore" />
            </Button>
          </GridColumn>
        </Grid>
      </Section>
    </div>
  );
};
