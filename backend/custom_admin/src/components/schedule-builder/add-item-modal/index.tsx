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
        <Dialog.Description size="2" mb="4" color="gray">
          Search an existing proposal or keynote, or create a custom event for
          this slot.
        </Dialog.Description>
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
