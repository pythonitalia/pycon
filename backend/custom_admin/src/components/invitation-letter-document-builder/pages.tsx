import { Button, Card, Flex, Heading, Separator, Text } from "@radix-ui/themes";
import { Plus } from "lucide-react";

import { Fragment } from "react";
import { EditorSection } from "./editor-section";
import { useLocalData } from "./local-state";
import { PageLayoutOptions } from "./page-layout-option";

export const Pages = () => {
  const { getPages, addPage } = useLocalData();
  const pages = getPages();

  return (
    <Card size="3">
      <Flex direction="column" gap="1" mb="5">
        <Heading as="h2" size="5">
          Pages
        </Heading>
        <Text color="gray" size="2">
          The body of the document. Pages are rendered in order.
        </Text>
      </Flex>

      <PageLayoutOptions />

      <Separator size="4" my="5" />

      <Flex direction="column" gap="5">
        {pages.map((page, index) => (
          <Fragment key={page.id}>
            {index > 0 && <Separator size="4" />}
            <EditorSection title={page.title} pageId={page.id} />
          </Fragment>
        ))}
      </Flex>

      <Flex mt="5">
        <Button variant="soft" size="2" onClick={addPage}>
          <Plus size={16} />
          Add page
        </Button>
      </Flex>
    </Card>
  );
};
