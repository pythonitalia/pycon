import React from "react";

import { Heading, Text } from "fannypack";
import styled from "styled-components";
import { STANDARD_CUSTOM_COLUMNS_PADDING } from "../../config/spacing";
import { CustomColumn } from "../column";
import { CustomColumns } from "../columns";
import { SectionTitle } from "../section-title";

const Wrapper = styled.div``;

export const Events = () => {
  return (
    <Wrapper>
      <CustomColumns
        paddingLeft={STANDARD_CUSTOM_COLUMNS_PADDING}
        paddingRight={STANDARD_CUSTOM_COLUMNS_PADDING}
      >
        <CustomColumn>
          <SectionTitle>EVENTS</SectionTitle>
        </CustomColumn>
      </CustomColumns>
      <CustomColumns
        marginTop={{ desktop: -4, tablet: -4, mobile: -1 }}
        paddingLeft={STANDARD_CUSTOM_COLUMNS_PADDING}
        paddingRight={STANDARD_CUSTOM_COLUMNS_PADDING}
      >
        <CustomColumn
          paddingRight={{ desktop: 3, tablet: 2, mobile: 0 }}
          spreadMobile={12}
          spread={6}
          spreadDesktop={12}
        >
          <Heading use="h3">Where is the venue?</Heading>
          <Text>
            Lorem ipsum, dolor sit amet consectetur adipisicing elit. Quibusdam
            numquam inventore laboriosam quisquam nobis maxime reiciendis a
            consectetur nisi temporibus. Quo autem magni eaque suscipit
            obcaecati ad excepturi iste ab!
          </Text>
        </CustomColumn>
        <CustomColumn
          paddingRight={{ desktop: 3, tablet: 2, mobile: 0 }}
          spreadMobile={12}
          spread={6}
          spreadDesktop={12}
        >
          <Heading use="h3">When will the event take place?</Heading>
          <Text>
            Lorem ipsum, dolor sit amet consectetur adipisicing elit. Quibusdam
            numquam inventore laboriosam quisquam nobis maxime reiciendis a
            consectetur nisi temporibus. Quo autem magni eaque suscipit
            obcaecati ad excepturi iste ab!
          </Text>
        </CustomColumn>
        <CustomColumn
          marginTop={{ desktop: 2, tablet: 2, mobile: 0 }}
          paddingRight={{ desktop: 3, tablet: 2, mobile: 0 }}
          spreadMobile={12}
          spread={6}
          spreadDesktop={12}
        >
          <Heading use="h3">How can I contribute?</Heading>
          <Text>
            Lorem ipsum, dolor sit amet consectetur adipisicing elit. Quibusdam
            numquam inventore laboriosam quisquam nobis maxime reiciendis a
            consectetur nisi temporibus. Quo autem magni eaque suscipit
            obcaecati ad excepturi iste ab!
          </Text>
        </CustomColumn>
        <CustomColumn
          marginTop={{ desktop: 2, tablet: 2, mobile: 0 }}
          paddingRight={{ desktop: 3, tablet: 2, mobile: 0 }}
          spreadMobile={12}
          spread={6}
          spreadDesktop={12}
        >
          <Heading use="h3">Where is the venue?</Heading>
          <Text>
            Lorem ipsum, dolor sit amet consectetur adipisicing elit. Quibusdam
            numquam inventore laboriosam quisquam nobis maxime reiciendis a
            consectetur nisi temporibus. Quo autem magni eaque suscipit
            obcaecati ad excepturi iste ab!
          </Text>
        </CustomColumn>
      </CustomColumns>
    </Wrapper>
  );
};
