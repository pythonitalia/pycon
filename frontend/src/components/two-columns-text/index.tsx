import React from "react";

import { Heading, Text } from "fannypack";
import { Column, Row } from "grigliata";
import styled from "styled-components";
import { STANDARD_ROW_PADDING } from "../../config/spacing";

const Base = styled.div`
  position: relative;
  padding: 0;
  margin: 2rem 0;

  .background_image {
    width: 100%;
    height: 100%;
    position: absolute;
    display: flex;
    right: 0;
    top: 0;
    img {
      max-width: 100%;
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
    padding: 4rem 0;

    @media (min-width: 1024px) {
      padding: 6rem 0;
    }
    @media (min-width: 1366px) {
      padding: 12rem 0;
    }
    position: relative;
    z-index: 3;
  }
`;

export const TwoColumnsText = () => {
  return (
    <Base>
      <div className="background_image">
        <div className="background_image__container">
          <div className="background_image__overlay" />
          <img src="https://placebear.com/600/400" alt="" />
        </div>
      </div>
      <div className="columns_wrapper">
        <Row
          paddingLeft={STANDARD_ROW_PADDING}
          paddingRight={STANDARD_ROW_PADDING}
        >
          <Column
            columnWidth={{
              mobile: 12,
              tabletPortrait: 6,
              tabletLandscape: 5,
              desktop: 5,
            }}
          >
            <Heading use="h2">Why Pycon?</Heading>
            <Text>
              Lorem ipsum dolor sit amet consectetur, adipisicing elit. Sequi
              excepturi nostrum harum minima esse corrupti possimus voluptatum
              amet atque illum, maiores tempore? At in, dolorem recusandae nihil
              inventore quasi reiciendis?
            </Text>
          </Column>
          <Column
            columnWidth={{
              mobile: 12,
              tabletPortrait: 6,
              tabletLandscape: 5,
              desktop: 5,
            }}
            marginTop={{
              mobile: 2,
              tabletPortrait: 0,
              tabletLandscape: 0,
              desktop: 0,
            }}
          >
            <Heading use="h2">Why Pycon?</Heading>
            <Text>
              Lorem ipsum dolor sit amet consectetur, adipisicing elit. Sequi
              excepturi nostrum harum minima esse corrupti possimus voluptatum
              amet atque illum, maiores tempore? At in, dolorem recusandae nihil
              inventore quasi reiciendis?
            </Text>
          </Column>
        </Row>
      </div>
    </Base>
  );
};
