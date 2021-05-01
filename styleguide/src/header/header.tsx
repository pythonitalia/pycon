import React from "react";
import { Logo } from "../logo/logo";
import { MenuButton } from "../menu-button/menu-button";

export const Header = () => (
  <header className="p-8 flex justify-between max-w-7xl mx-auto">
    <Logo className="w-40" />
    <MenuButton />
  </header>
);
