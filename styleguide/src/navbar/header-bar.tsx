import clsx from "clsx";
import React from "react";

import { Container } from "../container";
import { ActionItem } from "./action-item";
import { Action } from "./types";

type HeaderBarProps = {
  hidden?: boolean;
  actions: Action[];
  logo: React.JSXElementConstructor<any>;
  mobileLogo: React.JSXElementConstructor<any>;
};

export const HeaderBar = ({
  actions,
  hidden,
  logo: Logo,
  mobileLogo: MobileLogo,
}: HeaderBarProps) => {
  return (
    <Container
      className={clsx("z-[1050] relative", {
        invisible: hidden,
      })}
    >
      <div className="flex justify-between items-center py-6 lg:py-10">
        <div className="lg:hidden h-full">
          <a href="/">
            <MobileLogo className="w-28" />
          </a>
        </div>
        <div className="hidden lg:block h-full">
          <a href="/">
            <Logo className="w-64" />
          </a>
        </div>
        <div className="flex">
          {actions.map((action, index) => (
            <ActionItem
              key={action.text}
              {...action}
              onClick={action.onClick}
              className={
                index !== actions.length - 1 && index !== 0
                  ? "border-l-0 border-r-0"
                  : ""
              }
            />
          ))}
        </div>
      </div>
    </Container>
  );
};
