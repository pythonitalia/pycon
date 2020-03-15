import { Item } from "./types";

// TODO: let's be consistent with naming (training vs tutorial)
export const isTraining = (item: Item) => {
  if (item.submission) {
    return item.submission.type!.name.toLowerCase() === "tutorial";
  }

  return item.type.toLowerCase() === "training";
};
