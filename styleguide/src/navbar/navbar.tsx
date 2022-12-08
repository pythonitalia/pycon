import React, { useState } from "react";
import { Separator } from "../separator";
import { HeaderBar } from "./header-bar";
import { Menu } from "./menu";
import { Action, Link as LinkType } from "./types";

type Props = {
  logo: React.JSXElementConstructor<any>;
  mobileLogo: React.JSXElementConstructor<any>;
  actions: Action[];
  mainLinks: LinkType[];
  secondaryLinks: LinkType[];
  bottomBarLink?: LinkType;
};

export const NavBar = ({
  logo,
  mobileLogo,
  mainLinks,
  secondaryLinks,
  actions: closedMenuActions,
  bottomBarLink,
}: Props) => {
  const [isOpen, setOpenMenu] = useState(false);
  const toggleMenu = () => setOpenMenu((open) => !open);
  const openMenuActions: Action[] = [
    {
      icon: "close",
      onClick: toggleMenu,
    },
  ];
  const baseMenuAction: Action = {
    text: "Menu",
    icon: "menu",
    onClick: toggleMenu,
  };

  const actions = isOpen
    ? openMenuActions
    : [...closedMenuActions, baseMenuAction];

  return (
    <>
      <HeaderBar actions={actions} mobileLogo={mobileLogo} logo={logo} />
      {isOpen && (
        <div className="bg-purple absolute top-0 left-0 w-full h-fit z-40">
          <HeaderBar
            actions={actions}
            mobileLogo={mobileLogo}
            logo={logo}
            hidden
          />

          <Menu
            mainLinks={mainLinks}
            secondaryLinks={secondaryLinks}
            bottomBarLink={bottomBarLink}
          />

          <Separator />
        </div>
      )}
    </>
  );
};
