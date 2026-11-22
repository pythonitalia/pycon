import { Flex, Heading, Link, TabNav } from "@radix-ui/themes";
import { useEffect, useState } from "react";
import { useArgs } from "../shared/args";
import type { Screen } from "./types";

const NAV_ACTIONS_ID = "review-beta-nav-actions";

export const useNavActionsSlot = () => {
  const [slot, setSlot] = useState<HTMLElement | null>(null);
  useEffect(() => setSlot(document.getElementById(NAV_ACTIONS_ID)), []);
  return slot;
};

export const ReviewBetaNav = () => {
  const { screens, screen: currentScreenId } = useArgs() as {
    screens: Screen[];
    screen: string;
  };

  const currentScreen = screens.find((screen) => screen.id === currentScreenId);
  const areaScreens = screens.filter(
    (screen) => screen.area === currentScreen?.area,
  );
  const otherArea = screens.find(
    (screen) => screen.area !== currentScreen?.area,
  );

  return (
    <Flex direction="column" gap="2" mb="5">
      <Heading size="4">{currentScreen?.area_title}</Heading>
      <Flex
        align="center"
        justify="between"
        gap="4"
        className="shadow-[inset_0_-1px_0_0_var(--gray-a5)]"
      >
        <TabNav.Root aria-label={currentScreen?.area_title}>
          {areaScreens.map((screen) => (
            <TabNav.Link
              key={screen.id}
              href={screen.url}
              active={screen.id === currentScreenId}
            >
              {screen.title}
            </TabNav.Link>
          ))}
        </TabNav.Root>
        <Flex gap="4" align="center">
          <div id={NAV_ACTIONS_ID} />
          {otherArea && (
            <Link size="2" href={otherArea.url}>
              {otherArea.area_title} →
            </Link>
          )}
        </Flex>
      </Flex>
    </Flex>
  );
};
