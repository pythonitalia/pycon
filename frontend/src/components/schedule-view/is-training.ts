import { Item } from "./types";

// TODO: let's be consistent with naming (training vs tutorial)
export const isTraining = (item: Item) => {
  // TODO Remove for now and only use the item type to check
  // if (item.submission) {
  //   return item.submission.type!.name.toLowerCase() === "tutorial";
  // }

  return item.type.toLowerCase() === "training";
};
