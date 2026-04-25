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

type Props = {
  children: React.ReactNode;
  options: SelectProps[];
  onConfirm?: () => void;
  onRemove?: () => void;
  onChange?: (id: string, e: any) => void;
  action: "add" | "remove";
};

export const CardPartOptions = ({
  children,
  options,
  onChange,
  onConfirm,
  onRemove,
  action,
}: Props) => {
  return (
    <div className="bg-milk grid lg:grid-cols-cardpart-options divide-y lg:divide-y-[0px] lg:divide-x">
      <SideText className="hidden lg:flex">{children}</SideText>
      <div
        className="grid lg:grid-cols-cardpart-options-options !border-t-0 divide-y lg:divide-y-[0px] lg:divide-x"
        style={
          {
            "--num-of-options": options.length,
          } as CSSProperties
        }
      >
        {options?.map((select) => (
          <Action key={select.id} noPadding>
            <SimpleSelect
              disabled={action === "remove"}
              onChange={(e) => onChange?.(select.id, e)}
              className={clsx("pl-4 py-7 lg:pl-5", {
                "pr-9 lg:pr-14": action === "add",
              })}
              value={select.value}
              options={select.options}
              placeholder={select.placeholder}
            />
          </Action>
        ))}

        <div className="grid grid-cols-[1fr_auto] divide-x lg:divide-x-[0px]">
          <SideText className="lg:hidden">{children}</SideText>

          {action === "add" && (
            <Action onClick={onConfirm} button>
              <PlusIcon />
            </Action>
          )}
          {action === "remove" && (
            <Action negative onClick={onRemove} button>
              <MinusIcon />
            </Action>
          )}
        </div>
      </div>
    </div>
  );
};
