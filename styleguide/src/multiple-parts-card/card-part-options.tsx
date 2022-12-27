import clsx from "clsx";
import React, { CSSProperties } from "react";
import { MinusIcon } from "../icons/minus";
import { PlusIcon } from "../icons/plus";
import { Option, SimpleSelect } from "../simple-select/simple-select";
import { Action } from "./action";
import { SideText } from "./sidetext";

type SelectProps = {
  id: string;
  value?: string;
  options: Option[];
  placeholder?: string | React.ReactNode;
};

type Props = React.PropsWithChildren<{
  options: SelectProps[];
  onConfirm?: () => void;
  onRemove?: () => void;
  onChange?: (id: string, e: any) => void;
  action: "add" | "remove";
}>;

export const CardPartOptions = ({
  children,
  options,
  onChange,
  onConfirm,
  onRemove,
  action,
}: Props) => {
  return (
    <div className="bg-cream flex flex-col justify-start lg:flex-row lg:justify-between">
      <SideText>{children}</SideText>
      <div
        className="grid lg:grid-cols-cardpart-options"
        style={
          {
            "--num-of-options": options.length,
          } as CSSProperties
        }
      >
        {options?.map((select) => (
          <Action key={select.id} breakpoint="lg" noPadding noBorderMobile>
            <SimpleSelect
              disabled={action === "remove"}
              onChange={(e) => onChange?.(select.id, e)}
              className={clsx("pl-4 pr-9 lg:pr-14 py-7 lg:pl-5")}
              value={select.value}
              options={select.options}
              placeholder={select.placeholder}
            />
          </Action>
        ))}

        {action === "add" && (
          <Action onClick={onConfirm} breakpoint="lg" button noBorderMobile>
            <PlusIcon />
          </Action>
        )}
        {action === "remove" && (
          <Action negative onClick={onRemove} breakpoint="lg" button>
            <MinusIcon />
          </Action>
        )}
      </div>
    </div>
  );
};
