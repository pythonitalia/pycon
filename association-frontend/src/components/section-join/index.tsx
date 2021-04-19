import React, { useState } from "react";

import { SectionItem } from "~/components/section-item";

import { Button } from "../button";
import { ModalSigning } from "../modal-signing";

export const SectionJoin = () => {
  const [showModal, setShowModal] = useState(false);
  const toggleModal = () => {
    setShowModal(!showModal);
  };
  return (
    <>
      <ModalSigning showModal={showModal} closeModalHandler={toggleModal} />
      <SectionItem
        title={"Vuoi unirti?"}
        textTheme={"white"}
        withBackground={true}
        backgroundImageClass={"bg-reception-desk-pycon-10"}
      >
        <div className="lg:flex-shrink-0">
          <div className="inline-flex rounded-md shadow">
            <Button text={"Unisciti ora"} onClick={toggleModal} />
            {/* <a
            href="#"
            className="inline-flex items-center justify-center px-5 py-3 text-base font-medium text-white bg-indigo-600 border border-transparent rounded-md hover:bg-indigo-700"
          >
            Crea/Entra nel tuo account
          </a> */}
          </div>
        </div>
      </SectionItem>
    </>
  );
};
