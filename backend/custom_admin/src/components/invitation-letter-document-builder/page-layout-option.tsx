import { Flex, Text } from "@radix-ui/themes";
import { useLocalData } from "./local-state";
import { MarginInput } from "./margin-input";

export const PageLayoutOptions = () => {
  const { getPageLayout, setPageLayoutProperty } = useLocalData();

  const pageLayout = getPageLayout();

  return (
    <Flex direction="column" gap="3">
      <Text size="2" weight="medium">
        Layout options for all pages
      </Text>
      <MarginInput
        value={pageLayout.margin}
        onChange={(margin) => setPageLayoutProperty("margin", margin)}
      />
    </Flex>
  );
};
