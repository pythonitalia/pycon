import {
  AlertDialog,
  Box,
  Button,
  Dialog,
  Flex,
  Heading,
  IconButton,
  Text,
  TextField,
} from "@radix-ui/themes";
import { MoveDown, MoveUp, Pencil, Trash } from "lucide-react";
import { RichEditor } from "../shared/rich-editor";
import { HideNode } from "../shared/rich-editor/menu-bar";
import { useLocalData } from "./local-state";
import { RunningElementsOptions } from "./running-elements-options";

export const EditorSection = ({
  title,
  pageId,
}: {
  title: string;
  pageId: string;
}) => {
  const {
    movePageUp,
    movePageDown,
    removePage,
    renamePage,
    setContent,
    getContent,
  } = useLocalData();
  const isPage = pageId !== "header" && pageId !== "footer";

  const onMoveUp = () => movePageUp(pageId);
  const onMoveDown = () => movePageDown(pageId);
  const onRemove = () => removePage(pageId);
  const onRename = (value: string) => renamePage(pageId, value);
  const onUpdate = (content: string) => setContent(pageId, content);

  const content = getContent(pageId);

  return (
    <Box>
      <Flex align="center" justify="between" gap="3" mb="3">
        {isPage ? (
          <EditableTitle value={title} onRename={onRename} />
        ) : (
          <Heading size="3">{title}</Heading>
        )}
        {isPage && (
          <Flex align="center" gap="1">
            <IconButton
              variant="ghost"
              color="gray"
              onClick={onMoveUp}
              aria-label="Move page up"
            >
              <MoveUp size={16} />
            </IconButton>
            <IconButton
              variant="ghost"
              color="gray"
              onClick={onMoveDown}
              aria-label="Move page down"
            >
              <MoveDown size={16} />
            </IconButton>
            <RemovePage onRemove={onRemove} />
          </Flex>
        )}
      </Flex>

      {!isPage && (
        <Box mb="3">
          <RunningElementsOptions pageId={pageId} />
        </Box>
      )}

      <RichEditor
        hide={[HideNode.buttonNode, HideNode.link]}
        content={content}
        onUpdate={onUpdate}
      />
    </Box>
  );
};

const RemovePage = ({ onRemove }: { onRemove: () => void }) => {
  return (
    <AlertDialog.Root>
      <AlertDialog.Trigger>
        <IconButton color="crimson" variant="ghost" aria-label="Remove page">
          <Trash size={16} />
        </IconButton>
      </AlertDialog.Trigger>

      <AlertDialog.Content maxWidth="450px">
        <AlertDialog.Title>Remove page</AlertDialog.Title>
        <AlertDialog.Description size="2">
          Are you sure you want to remove this page?
        </AlertDialog.Description>
        <Flex gap="3" mt="4" justify="end">
          <AlertDialog.Cancel>
            <Button variant="soft" color="gray">
              Cancel
            </Button>
          </AlertDialog.Cancel>
          <AlertDialog.Action>
            <Button color="crimson" onClick={onRemove}>
              Remove
            </Button>
          </AlertDialog.Action>
        </Flex>
      </AlertDialog.Content>
    </AlertDialog.Root>
  );
};

const EditableTitle = ({
  value,
  onRename,
}: { value: string; onRename: (value: string) => void }) => {
  return (
    <Dialog.Root>
      <Dialog.Trigger>
        <Button variant="soft" size="2">
          {value}
          <Pencil size={16} />
        </Button>
      </Dialog.Trigger>
      <Dialog.Content maxWidth="450px">
        <Dialog.Title>Rename page</Dialog.Title>
        <Dialog.Description size="2" mb="4">
          This name is only used internally and will not be visible in the
          output PDF.
        </Dialog.Description>
        <Flex direction="column" gap="3">
          <label>
            <Text as="div" size="2" mb="1" weight="bold">
              Name
            </Text>
            <TextField.Root
              defaultValue={value}
              placeholder="Name"
              onChange={(e) => onRename(e.target.value)}
            />
          </label>
        </Flex>
        <Flex gap="3" mt="4" justify="end">
          <Dialog.Close>
            <Button variant="soft" color="gray">
              Save
            </Button>
          </Dialog.Close>
        </Flex>
      </Dialog.Content>
    </Dialog.Root>
  );
};
