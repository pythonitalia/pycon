import * as React from "react";
import { Hero } from "../components/hero";
import { TwoColumnsText } from "../components/two-columns-text";
import { HomeLayout } from "../layouts/home";

export default () => (
  <HomeLayout>
    <Hero title="Hello world" backgroundImage={"https://placebear.com/1300/400"}>
      <p>
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Alias et omnis
        hic veniam nisi architecto reprehenderit voluptate magnam sed commodi
        vel quidem ea, blanditiis quos harum non ipsam, soluta saepe.
      </p>
    </Hero>
    <TwoColumnsText />
  </HomeLayout>
);
