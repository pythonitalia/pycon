import React from "react";

import { PythonSquare0, PythonSquare1, PythonSquare2, PythonSquare3 } from "./pythons";

type TicketProps = {
  name: string;
};

export const Ticket = ({ name }: TicketProps) => {
  return (
    <div>
      <div className="flex bg-white">
        <div className="flex w-full m-4 border-4 border-black border-solid">
          <div className="w-24 border-r-2 border-black border-solid min-w-min bg-purple">
            <PythonSquare0 />
          </div>
          <div className="flex items-center justify-center flex-grow">
            <div className="text-5xl font-bold ">PyFest</div>
          </div>
        </div>
      </div>

      <div className="flex border-t-4 border-b-4 border-black border-solid bg-purple">
        <div className="ml-4">
          <div className="my-3 text-5xl font-bold">{name}</div>
          <div className="my-2 text-xl text-white ">Made.com</div>
          <div className="my-2 ">@etty</div>
        </div>
      </div>

      <div className="flex border-b-4 border-black border-solid">
        <div className="w-1/3 px-2 pt-2 bg-green">
          <PythonSquare1 />
        </div>
        <div className="w-1/3 border-l-4 border-r-4 border-black border-solid bg-casablanca ">
          <PythonSquare2 />
        </div>
        <div className="w-1/3 bg-aquamarine ">
          <PythonSquare3 />
        </div>
      </div>
    </div>
  );
};
