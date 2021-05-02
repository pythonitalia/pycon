import "../style.css";

import React from "react";
import { Footer } from "../footer/footer";

type Props = {
  children: React.ReactNode;
};

export const Page = ({ children }: Props) => (
  <div className="divide-black divide-y-4">
    {children}

    <Footer />
  </div>
);
