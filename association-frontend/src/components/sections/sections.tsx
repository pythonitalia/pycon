import React from "react";
import SectionEvents from "~/components/section-events/section-events";
import SectionJoin from "~/components/section-join/section-join";
import SectionPythonIta from "~/components/section-python-ita/section-python-ita";
import SectionSocialMedia from "~/components/section-social-media/section-social-media";
import Modal from "../modal/modal";

import SectionPyConIta from "../section-pycon-ita/section-pycon-ita";

const Sections = () => {
  return (
    <>
      <SectionPythonIta />
      <SectionPyConIta />
      <SectionJoin />
    </>
  );
};

export default Sections;
