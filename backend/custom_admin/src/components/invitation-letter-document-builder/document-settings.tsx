import { Box, Button, Card, Heading, Text } from "@radix-ui/themes";
import { EditorSection } from "./editor-section";

export const DocumentSettings = () => {
  return (
    <Card>
      <Heading as="h1">Document</Heading>
      <Box height="var(--space-2)" />
      <Text>Header and footer are shared across all pages.</Text>

      <Box height="var(--space-5)" />

      <EditorSection title="Header" pageId="header" />
      <Box height="var(--space-5)" />

      <EditorSection title="Footer" pageId="footer" />
    </Card>
  );
};
