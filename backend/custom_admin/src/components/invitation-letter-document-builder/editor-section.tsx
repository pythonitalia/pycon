import {
  AlertDialog,
  Button,
  Dialog,
  Flex,
  Heading,
  Text,
  TextField,
  Theme,
} from "@radix-ui/themes";
import { Box } from "@radix-ui/themes";
import { MoveDown, MoveUp, Pencil, Trash } from "lucide-react";
import { RichEditor } from "../shared/rich-editor";
import { useLocalData } from "./local-state";

export const EditorSection = ({
  title,
  content,
  pageId,
}: {
  title: string;
  content: string;
  pageId: string;
}) => {
  const { movePageUp, movePageDown, removePage, renamePage, setContent } =
    useLocalData();
  const isPage = pageId !== "header" && pageId !== "footer";

  const onMoveUp = () => movePageUp(pageId);
  const onMoveDown = () => movePageDown(pageId);
  const onRemove = () => removePage(pageId);
  const onRename = (value: string) => renamePage(pageId, value);
  const onUpdate = (content: string) => setContent(pageId, content);

  return (
    <Box>
      <Flex align="center" gap="3">
        {isPage && <EditableTitle value={title} onRename={onRename} />}
        {!isPage && <Heading size="2">{title}</Heading>}
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
        {isPage && <RemovePage onRemove={onRemove} />}
      </Flex>
      <Box height="var(--space-3)" />
      <RichEditor content={content} onUpdate={onUpdate} />
    </Box>
  );
};

const RemovePage = ({ onRemove }: { onRemove: () => void }) => {
  return (
    <AlertDialog.Root>
      <AlertDialog.Trigger>
        <Button color="crimson" variant="ghost">
          <Trash size={16} />
        </Button>
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
