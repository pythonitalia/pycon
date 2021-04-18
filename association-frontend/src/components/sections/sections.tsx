import React from "react";

import SectionJoin from "~/components/section-join/section-join";
import SectionPythonIta from "~/components/section-python-ita/section-python-ita";

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
