import { Button, Card, Heading } from "@radix-ui/themes";
import { Box } from "@radix-ui/themes";
import { Plus } from "lucide-react";

import { Fragment } from "react";
import { EditorSection } from "./editor-section";
import { useLocalData } from "./local-state";
import { PageLayoutOptions } from "./page-layout-option";

export const Pages = () => {
  const { getPages, addPage } = useLocalData();
  const pages = getPages();

  return (
    <Card>
      <Heading>Pages</Heading>
      <Box height="var(--space-1)" />

      <PageLayoutOptions />

      <Box height="var(--space-5)" />

      {pages.map((page) => (
        <Fragment key={page.id}>
          <EditorSection title={page.title} pageId={page.id} />
          <Box height="var(--space-3)" />
        </Fragment>
      ))}

      <Box height="var(--space-2)" />
      <Button variant="soft" onClick={addPage}>
        <Plus size={16} />
        Add Page
      </Button>
    </Card>
  );
};
