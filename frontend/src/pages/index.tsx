import * as React from "react";

import styled from "styled-components";
import { Hero } from "../components/hero";
import { HomeLayout } from "../layouts/home";

export default () => (
  <HomeLayout>
    <Hero
      backgroundImage={
        "https://live.staticflickr.com/65535/33985680028_8eb0b570f9_h.jpg"
      }
    />
  </HomeLayout>
);
