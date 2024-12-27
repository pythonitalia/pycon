import * as Toolbar from "@radix-ui/react-toolbar";
import { Tooltip } from "@radix-ui/themes";
import clsx from "clsx";

export const ToolbarButton = ({
  children,
  isActive = false,
  disabled = false,
  tooltip = "",
  ...props
}) => (
  <Tooltip content={tooltip}>
    <Toolbar.Button
      disabled={disabled}
      className={clsx("p-2 rounded hover:bg-gray-200 transition-opacity", {
        "bg-gray-200": isActive,
        "opacity-20": disabled,
      })}
      {...props}
    >
      {children}
    </Toolbar.Button>
  </Tooltip>
);
