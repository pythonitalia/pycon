import React from "react";

import Head from "next/head";

import Sections from "~/components/sections/sections";

export default function Home() {
  return (
    <div>
      <Head>
        <title>Associazione Python Italia</title>
        <link rel="icon" href="/favicon.png" />
      </Head>
      <Sections />
    </div>
  );
}
