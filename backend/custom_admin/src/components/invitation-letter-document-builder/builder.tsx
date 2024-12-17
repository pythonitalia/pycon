import * as AlertDialog from "@radix-ui/react-alert-dialog";
import { Button, Flex, Heading, Text, Theme } from "@radix-ui/themes";
import { Box } from "@radix-ui/themes";
import { MoveDown, MoveUp, Plus, Trash } from "lucide-react";
import { Fragment, useEffect, useState } from "react";
import type { InvitationLetterDocumentStructure } from "../../types";
import { Base } from "../shared/base";
import { DjangoAdminLayout } from "../shared/django-admin-layout";
import { Editor } from "./editor";
import { EditorSection } from "./editor-section";
import { useInvitationLetterDocumentQuery } from "./invitation-letter-document.generated";
import { useLocalData } from "./local-state";
import { useUpdateInvitationLetterDocumentMutation } from "./update-invitation-letter-document.generated";

export const InvitationLetterBuilder = () => {
  const { localData, saveChanges, isSaving, addPage } = useLocalData();

  if (!localData) {
    return <Text>Loading...</Text>;
  }

  return (
    <>
      <Box height="var(--space-3)" />

      <Box className="border-gray-300 rounded border-2" p="3">
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
      </Box>

      <Box height="var(--space-5)" />

      <Box className="border-gray-300 rounded border-2" p="3">
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
      </Box>

      <Box height="var(--space-3)" />
      <Box position="sticky" bottom="0" p="3" className="bg-white">
        <Button onClick={saveChanges} loading={isSaving}>
          Save changes
        </Button>
      </Box>
    </>
  );
};
