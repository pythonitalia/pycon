import Head from "next/head";
import React from "react";
import Footer from "~/components/footer/footer";
import Header from "~/components/header/header";
import Hero from "~/components/hero/hero";
import SectionHelp from "~/components/section-help";
import Sections from "~/components/sections/sections";

export default function Home() {
  return (
    <div>
      <Head>
        <title>Associazione Python Italia</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="bg-white">
        <Header />
        <main>
          {/* Hero section */}
          <Hero />

          {/* Alternating Feature Sections */}
          <Sections />
          {/* Stats section */}
          {/* <StatsPanel/> */}
          {/* CTA Section */}
          <SectionHelp />
        </main>

        <Footer />
      </div>
    </div>
  );
}
