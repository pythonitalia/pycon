import { Button, Card, Heading } from "@radix-ui/themes";
import { Plus } from "lucide-react";

import { Fragment } from "react";
import { Spacer } from "../shared/spacer";
import { EditorSection } from "./editor-section";
import { useLocalData } from "./local-state";
import { PageLayoutOptions } from "./page-layout-option";

export const Pages = () => {
  const { getPages, addPage } = useLocalData();
  const pages = getPages();

  return (
    <Card>
      <Heading>Pages</Heading>

      <Spacer size={1} />

      <PageLayoutOptions />

      <Spacer size={5} />

      {pages.map((page) => (
        <Fragment key={page.id}>
          <EditorSection title={page.title} pageId={page.id} />
          <Spacer />
        </Fragment>
      ))}

      <Spacer size={2} />

      <Button variant="soft" onClick={addPage}>
        <Plus size={16} />
        Add Page
      </Button>
    </Card>
  );
};
