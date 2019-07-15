import React from "react";

type ButtonProps = {
  children: React.ReactNode;
  color: string;
};

export const Button = (props: ButtonProps) => <button>{props.children}</button>;
