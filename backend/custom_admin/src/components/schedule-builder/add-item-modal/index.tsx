import { Dialog, Flex } from "@radix-ui/themes";
import { AddCustomEvent } from "./add-custom-event";
import { useAddItemModal } from "./context";
import { SearchEvent } from "./search-event";

export const AddItemModal = () => {
  const { isOpen, close, data } = useAddItemModal();

  return (
    <Dialog.Root open={isOpen} onOpenChange={(open) => !open && close()}>
      <Dialog.Content maxWidth="768px">
        <Dialog.Title>Add event to schedule</Dialog.Title>
        {/* data is null while the dialog animates closed; guard so children
            (which read data.day/slot/room) never dereference null. */}
        {data && (
          <Flex direction="column" gap="5">
            <SearchEvent />
            <AddCustomEvent />
          </Flex>
        )}
      </Dialog.Content>
    </Dialog.Root>
  );
};
