import { Button, Card, Heading, Text } from "@radix-ui/themes";
import { Box } from "@radix-ui/themes";
import { Plus } from "lucide-react";
import { Fragment, useEffect } from "react";

import { EditorSection } from "./editor-section";
import { useLocalData } from "./local-state";

export const InvitationLetterBuilder = () => {
  const { isDirty, localData, saveChanges, isSaving, addPage } = useLocalData();

  useEffect(() => {
    const listener = (e) => {
      if (isDirty) {
        e.preventDefault();
        e.returnValue = "";
      }

      return "";
    };

    window.addEventListener("beforeunload", listener);

    return () => {
      window.removeEventListener("beforeunload", listener);
    };
  }, [isDirty]);

  return (
    <>
      <Box height="var(--space-3)" />

      <Card>
        <Heading as="h1">Document</Heading>
        <Box height="var(--space-2)" />
        <Text>Header and footer are shared across all pages.</Text>

        <Box height="var(--space-5)" />

        <EditorSection
          title="Header"
          content={localData.header}
          pageId="header"
        />
        <Box height="var(--space-5)" />

        <EditorSection
          title="Footer"
          content={localData.footer}
          pageId="footer"
        />
      </Card>

      <Box height="var(--space-5)" />

      <Card>
        <Heading>Pages</Heading>
        <Box height="var(--space-5)" />

        {localData.pages.map((page) => (
          <Fragment key={page.id}>
            <EditorSection
              title={page.title}
              content={page.content}
              pageId={page.id}
            />
            <Box height="var(--space-3)" />
          </Fragment>
        ))}

        <Box height="var(--space-2)" />
        <Button variant="soft" onClick={addPage}>
          <Plus size={16} />
          Add Page
        </Button>
      </Card>

      <Box height="var(--space-3)" />
      <Box position="sticky" bottom="0" p="3" className="bg-white">
        <Button onClick={saveChanges} loading={isSaving}>
          Save changes
        </Button>
      </Box>
    </>
  );
};
