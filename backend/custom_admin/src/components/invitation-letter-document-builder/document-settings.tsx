import { Card, Flex, Heading, Separator, Text } from "@radix-ui/themes";
import { EditorSection } from "./editor-section";

export const DocumentSettings = () => {
  return (
    <Card size="3">
      <Flex direction="column" gap="1" mb="5">
        <Heading as="h2" size="5">
          Header &amp; footer
        </Heading>
        <Text color="gray" size="2">
          Shared across every page of the document.
        </Text>
      </Flex>

      <Flex direction="column" gap="5">
        <EditorSection title="Header" pageId="header" />
        <Separator size="4" />
        <EditorSection title="Footer" pageId="footer" />
      </Flex>
    </Card>
  );
};
