import { Card, Heading, Text } from "@radix-ui/themes";
import { Spacer } from "../shared/spacer";
import { EditorSection } from "./editor-section";

export const DocumentSettings = () => {
  return (
    <Card>
      <Heading as="h1">Document</Heading>
      <Spacer />

      <Text>Header and footer are shared across all pages.</Text>

      <Spacer />

      <EditorSection title="Header" pageId="header" />
      <Spacer size={5} />

      <EditorSection title="Footer" pageId="footer" />
    </Card>
  );
};
