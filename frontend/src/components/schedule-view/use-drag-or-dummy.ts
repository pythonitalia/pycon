import {
  ConnectDragPreview,
  ConnectDragSource,
  DragObjectWithType,
  DragSourceHookSpec,
  useDrag,
} from "react-dnd";

export const useDragOrDummy = <
  DragObject extends DragObjectWithType,
  DropResult,
  CollectedProps,
>(
  spec: { adminMode?: boolean } & DragSourceHookSpec<
    DragObject,
    DropResult,
    CollectedProps
  >,
): [CollectedProps, ConnectDragSource, ConnectDragPreview] => {
  if (spec.adminMode) {
    // eslint-disable-next-line react-hooks/rules-of-hooks
    return useDrag(spec);
  }

  return [{} as CollectedProps, () => null, () => null];
};
