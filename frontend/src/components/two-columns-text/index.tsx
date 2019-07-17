import React from "react";

import { Heading, Text } from "fannypack";
import styled from "styled-components";
import { CustomColumn } from "../column";
import { CustomColumns } from "../columns";

const Base = styled.div`
  position: relative;
  padding: 0;
  margin: 4rem 0;
  @media (min-width: 1024px) {
    padding: 12rem 0;
  }
  .background_image {
    width: 100%;
    height: 100%;
    position: absolute;
    display: flex;

    right: 0;
    top: 0;
    img {
      height: 100%;
      display: none;
      @media (min-width: 768px) {
        display: block;
      }
    }
    .background_image__container {
      margin-left: auto;
      display: inline-block;
      height: 100%;
      position: relative;
    }
    .background_image__overlay {
      background: rgb(255, 255, 255);
      background: linear-gradient(
        90deg,
        rgba(255, 255, 255, 1) 0%,
        rgba(255, 255, 255, 0.9) 50%,
        rgba(255, 255, 255, 0.8) 100%
      );
      height: 100%;
      width: 100%;
      position: absolute;
      left: 0;
      top: 0;
      z-index: 1;
      display: none;
      @media (min-width: 768px) {
        display: inline-block;
      }
    }
  }
  .columns_wrapper {
    position: relative;
    z-index: 3;
  }
`;

export const TwoColumnsText = () => {
  return (
    <Base>
      <div className="background_image">
        <div className="background_image__container">
          <div className="background_image__overlay"/>
          <img src="https://placebear.com/600/400" alt="" />
        </div>
      </div>
      <div className="columns_wrapper">
        <CustomColumns
          paddingTop={{ desktop: 4, mobile: 3 }}
          paddingBottom={{ desktop: 4, mobile: 3 }}
          paddingLeft={{ desktop: 4, mobile: 3 }}
          paddingRight={{ desktop: 4, mobile: 3 }}
        >
          <CustomColumn paddingRight={{ desktop: 12, mobile: 3 }}>
            <Heading use="h2">Why Pycon?</Heading>
            <Text>
              Lorem ipsum dolor sit amet consectetur, adipisicing elit. Sequi
              excepturi nostrum harum minima esse corrupti possimus voluptatum
              amet atque illum, maiores tempore? At in, dolorem recusandae nihil
              inventore quasi reiciendis?
            </Text>
          </CustomColumn>
          <CustomColumn
            marginTop={{ desktop: 0, mobile: 3 }}
            paddingRight={{ desktop: 12, mobile: 3 }}
          >
            <Heading use="h2">Best conf ever!</Heading>
            <Text>
              Lorem ipsum dolor sit amet consectetur, adipisicing elit. Sequi
              excepturi nostrum harum minima esse corrupti possimus voluptatum
              amet atque illum, maiores tempore? At in, dolorem recusandae nihil
              inventore quasi reiciendis?
            </Text>
          </CustomColumn>
        </CustomColumns>
      </div>
    </Base>
  );
};
