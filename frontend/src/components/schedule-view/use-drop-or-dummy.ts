import {
  ConnectDropTarget,
  DragObjectWithType,
  DropTargetHookSpec,
  useDrop,
} from "react-dnd";

export const useDropOrDummy = <
  DragObject extends DragObjectWithType,
  DropResult,
  CollectedProps
>(
  spec: { adminMode: boolean } & DropTargetHookSpec<
    DragObject,
    DropResult,
    CollectedProps
  >,
): [CollectedProps, ConnectDropTarget] => {
  if (spec.adminMode) {
    return useDrop(spec);
  }

  return [{} as CollectedProps, () => null];
};
