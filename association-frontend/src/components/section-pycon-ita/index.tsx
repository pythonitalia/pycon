import React from "react";

import { SectionItem } from "~/components/section-item";

import { Button } from "../button";

export const SectionPyConIta = () => (
  <SectionItem
    title="PyCon Italia"
    textTheme="white"
    withBackground={true}
    overlay={true}
    overlayTheme="black-light"
    backgroundImageClass="bg-pycon-group-blue"
  >
    <p className="mx-auto mb-4 text-xl text-center text-white">
      Dalla nostra passione per Python è nata PyCon Italia.
      <br />
      Ogni anno organizziamo la più grande conferenza italiana su Python.
      <br />
      Ogni tanto diventiamo anche Europei, come nel 2011, 2012, 2013 e 2017,
      collaborando all’organizzazione di EuroPython.
    </p>
    <p className="mx-auto mt-12 text-xl text-center text-white select-none">
      <Button link={"https://pycon.it/en"} text="Visita il sito" />
    </p>
  </SectionItem>
);
