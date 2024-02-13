import { Modal } from "../../shared/modal";
import { AddCustomEvent } from "./add-custom-event";
import { useAddItemModal } from "./context";
import { SearchEvent } from "./search-event";

export const AddItemModal = () => {
  const { isOpen, close } = useAddItemModal();

  if (!isOpen) {
    return null;
  }

  return (
    <Modal
      isOpen={isOpen}
      onClose={close}
      className="p-3 max-w-3xl w-full max-h-[700px] overflow-scroll"
    >
      <div className="">
        <h2 className="text-xl">Add event to schedule</h2>
        <ul>
          <li className="mt-2">
            <SearchEvent />
          </li>
          <li className="mt-5">
            <AddCustomEvent />
          </li>
        </ul>
      </div>
    </Modal>
  );
};
