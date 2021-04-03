import React, { useState } from "react";

import SectionItem from "~/components/section-item/section-item";

import Button from "../button/button";
import ModalSigning from "../modal-signing/modal-signing";

const SectionJoin = () => {
  const [modalHidden, setModalHidden] = useState(true);
  return (
    <>
      <ModalSigning isHidden={modalHidden} />
      <SectionItem
        title={"Vuoi unirti?"}
        textTheme={"white"}
        withBackground={true}
        backgroundImageClass={"bg-reception-desk-pycon-10"}
      >
        <div className="lg:flex-shrink-0">
          <div className="inline-flex rounded-md shadow">
            <Button
              text={"Unisciti ora"}
              onClick={(e: React.MouseEvent) => setModalHidden(!modalHidden)}
            />
            {/* <a
            href="#"
            className="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
          >
            Crea/Entra nel tuo account
          </a> */}
          </div>
        </div>
      </SectionItem>
    </>
  );
};
export default SectionJoin;
