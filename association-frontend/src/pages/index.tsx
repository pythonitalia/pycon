import React from "react";

import Head from "next/head";

import Sections from "~/components/sections/sections";

export default function Home() {
  return (
    <div>
      <Head>
        <title>Associazione Python Italia</title>
        <link rel="icon" href="/favicon.png" />
        <link
          href="https://fonts.googleapis.com/css?family=Montserrat:300,700"
          rel="stylesheet"
        />{" "}
      </Head>
      <Sections />
    </div>
  );
}
