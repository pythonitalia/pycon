import React from "react";

import { SectionJoin } from "~/components/section-join";
import { SectionPyConIta } from "~/components/section-pycon-ita";
import { SectionPythonIta } from "~/components/section-python-ita";

const Home = () => (
  <>
    <SectionPythonIta />
    <SectionPyConIta />
    <SectionJoin />
  </>
);

export default Home;
