import moment from "moment";
import { useState } from "react";

import { Slot } from "./types";

export const useSlots = (): [Slot[], (duration: number) => void] => {
  const [slots, setSlots] = useState<Slot[]>([]);

  const addSlot = (duration: number) => {
    const lastSlot = slots.length > 0 ? slots[slots.length - 1] : null;

    const hour = lastSlot
      ? lastSlot.hour.clone().add(duration, "minutes")
      : moment()
          .hour(8)
          .minute(45);
    const offset = lastSlot ? lastSlot.offset + lastSlot.size : 0;

    setSlots([
      ...slots,
      {
        duration,
        hour,
        // we use this instead of duration to calculate the dimension on the grid
        size: 45,
        offset,
      },
    ]);
  };

  return [slots, addSlot];
};
