import * as AlertDialog from "@radix-ui/react-alert-dialog";
import { Button, Flex, Heading, Text, Theme } from "@radix-ui/themes";
import { Box } from "@radix-ui/themes";
import { MoveDown, MoveUp, Plus, Trash } from "lucide-react";
import { Fragment, useEffect, useState } from "react";
import type { InvitationLetterDocumentStructure } from "../../types";
import { Base } from "../shared/base";
import { DjangoAdminLayout } from "../shared/django-admin-layout";
import { Editor } from "./editor";
import { useInvitationLetterDocumentQuery } from "./invitation-letter-document.generated";
import { useLocalData } from "./local-state";
import { useUpdateInvitationLetterDocumentMutation } from "./update-invitation-letter-document.generated";

export const EditorSection = ({
  title,
  content,
  pageId,
}: {
  title: string;
  content: string;
  pageId: string;
}) => {
  const { movePageUp, movePageDown, removePage, setContent } = useLocalData();
  const isPage = pageId !== "header" && pageId !== "footer";

  const onMoveUp = () => movePageUp(pageId);
  const onMoveDown = () => movePageDown(pageId);
  const onRemove = () => removePage(pageId);
  const onUpdate = () => setContent(pageId, content);

  return (
    <AlertDialog.Root>
      <Box>
        <Flex align="center" gap="3">
          <Heading size="5" as="h2">
            {title}
          </Heading>
          {isPage && (
            <Button variant="ghost" onClick={onMoveUp}>
              <MoveUp size={16} />
            </Button>
          )}
          {isPage && (
            <Button variant="ghost" onClick={onMoveDown}>
              <MoveDown size={16} />
            </Button>
          )}
          {isPage && (
            <AlertDialog.Trigger asChild>
              <Button color="crimson" variant="ghost">
                <Trash size={16} />
              </Button>
            </AlertDialog.Trigger>
          )}
        </Flex>
        <Box height="var(--space-3)" />
        <Editor content={content} onUpdate={onUpdate} />
      </Box>

      <AlertDialog.Portal>
        <Theme>
          <AlertDialog.Overlay className="fixed inset-0 bg-gray-500/75 transition-opacity" />
          <AlertDialog.Content className="transform rounded-lg bg-white fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 shadow-xl">
            <Box p="4">
              <AlertDialog.Title>
                <Text weight="bold">Remove page</Text>
              </AlertDialog.Title>
              <AlertDialog.Description>
                <Text size="2">Are you sure you want to remove this page?</Text>
              </AlertDialog.Description>
            </Box>
            <Flex
              className="bg-gray-50 rounded-lg"
              align="center"
              justify="end"
              gap="3"
              p="4"
            >
              <AlertDialog.Cancel asChild>
                <Button variant="ghost">Cancel</Button>
              </AlertDialog.Cancel>
              <AlertDialog.Action asChild>
                <Button color="crimson" onClick={onRemove}>
                  Remove
                </Button>
              </AlertDialog.Action>
            </Flex>
          </AlertDialog.Content>
        </Theme>
      </AlertDialog.Portal>
    </AlertDialog.Root>
  );
};
