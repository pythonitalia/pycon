import React from "react";

import Head from "next/head";

import SectionHelp from "~/components/section-help";
import Sections from "~/components/sections/sections";

export default function Home() {
  return (
    <div>
      <Head>
        <title>Associazione Python Italia</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Sections />
    </div>
  );
}
