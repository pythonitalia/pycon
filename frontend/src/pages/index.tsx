import * as React from "react";

import styled from "styled-components";
import { Hero } from "../components/hero";
import { HomeLayout } from "../layouts/home";

export default () => (
  <HomeLayout>
    <Hero
      title="Hello world"
      backgroundImage={
        "https://live.staticflickr.com/65535/33985680028_8eb0b570f9_h.jpg"
      }
    >
      <p>
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Alias et omnis
        hic veniam nisi architecto reprehenderit voluptate magnam sed commodi
        vel quidem ea, blanditiis quos harum non ipsam, soluta saepe.
      </p>
    </Hero>
  </HomeLayout>
);
