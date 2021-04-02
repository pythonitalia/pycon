import React from "react";
import { Carousel } from "./carousel";

export default {
  title: "Carousel",
};

export const Standard = () => (
  <Carousel title="The speakers">
    <div className="bg-red-400"></div>
    <div className="bg-blue-400"></div>
    <div className="bg-purple-400"></div>
    <div className="bg-yellow-400"></div>
    <div className="bg-red-400"></div>
    <div className="bg-blue-400"></div>
    <div className="bg-purple-400"></div>
    <div className="bg-yellow-400"></div>
  </Carousel>
);
