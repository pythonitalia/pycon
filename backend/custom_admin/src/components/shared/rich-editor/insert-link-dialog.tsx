import { Button, Dialog, Flex, Text, TextField } from "@radix-ui/themes";
import { useEffect, useState } from "react";

export const InsertLinkDialogContent = ({ onSubmit, initialValue }) => {
  const [link, setLink] = useState(initialValue);
  const onChange = (e) => setLink(e.target.value);

  useEffect(() => {
    setLink(initialValue);
  }, [initialValue]);

  return (
    <Dialog.Content maxWidth="450px" aria-describedby={undefined}>
      <Dialog.Title>Insert Link</Dialog.Title>
      <form action={(_) => onSubmit(link)}>
        <Flex direction="column" gap="3">
          <label>
            <Text as="div" size="2" mb="1" weight="bold">
              Link
            </Text>
            <TextField.Root
              defaultValue={link}
              placeholder="Name"
              type="text"
              onChange={onChange}
            />
          </label>
        </Flex>
        <Flex gap="3" mt="4" justify="end" align="center">
          <Dialog.Close>
            <Button variant="ghost" color="gray">
              Close
            </Button>
          </Dialog.Close>
          <Dialog.Close>
            <Button variant="soft" type="submit">
              Save
            </Button>
          </Dialog.Close>
        </Flex>
      </form>
    </Dialog.Content>
  );
};
