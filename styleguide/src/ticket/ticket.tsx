import React from "react";
import { TicketWrapper } from "./wrapper";
import { Snape } from "./snape";
import { Logo } from "../logo/logo";

type TicketProps = {
  name: string;
};

export const Ticket = ({ name }: TicketProps) => {
  return (
    <div>
      <div className=" max-w-sm  ">
        <div className="flex max-w-sm">
          <div className="flex border-solid border-4 border-black max-w-sm m-4 w-full">
            <div className="w-24 min-w-min bg-purple border-solid border-r-2 border-black">
              <Snape />
            </div>
            <div className="flex flex-grow items-center justify-center">
              <div className=" font-bold text-5xl">PyFest</div>
            </div>
          </div>
        </div>

        <div className="flex border-solid border-t-4 border-b-4 border-black bg-purple">
          <div className="ml-4">
            <div className="font-bold text-5xl my-3">Ester Beltrami</div>
            <div className="my-2 text-xl  text-white ">Made.com</div>
            <div className="my-2 ">@etty</div>
          </div>
        </div>

        <div className="flex  border-solid border-b-4 border-black">
          <div className="w-1/3 bg-green ">
            <Snape />
          </div>
          <div className="w-1/3 bg-aquamarine border-solid border-l-4 border-r-4 border-black ">
            <Snape />
          </div>
          <div className="w-1/3 bg-casablanca ">
            <Snape />
          </div>
        </div>
      </div>
    </div>
  );
};
