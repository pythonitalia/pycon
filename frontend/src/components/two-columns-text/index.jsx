"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = __importDefault(require("react"));
const fannypack_1 = require("fannypack");
const grigliata_1 = require("grigliata");
const styled_components_1 = __importDefault(require("styled-components"));
const spacing_1 = require("../../config/spacing");
const Base = styled_components_1.default.div `
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
    @media (min-width: 768px) {
      padding: 4rem 0;
    }
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
exports.TwoColumnsText = () => (<Base>
    <div className="background_image">
      <div className="background_image__container">
        <div className="background_image__overlay"/>
        <img src="https://placebear.com/600/400" alt=""/>
      </div>
    </div>
    <div className="columns_wrapper">
      <grigliata_1.Row paddingLeft={spacing_1.STANDARD_ROW_PADDING} paddingRight={spacing_1.STANDARD_ROW_PADDING}>
        <grigliata_1.Column columnWidth={{
    mobile: 12,
    tabletPortrait: 6,
    tabletLandscape: 5,
    desktop: 5,
}}>
          <fannypack_1.Heading use="h2">Why Pycon?</fannypack_1.Heading>
          <fannypack_1.Text>
            Lorem ipsum dolor sit amet consectetur, adipisicing elit. Sequi
            excepturi nostrum harum minima esse corrupti possimus voluptatum
            amet atque illum, maiores tempore? At in, dolorem recusandae nihil
            inventore quasi reiciendis?
          </fannypack_1.Text>
        </grigliata_1.Column>
        <grigliata_1.Column columnWidth={{
    mobile: 12,
    tabletPortrait: 6,
    tabletLandscape: 5,
    desktop: 5,
}} marginTop={{
    mobile: 2,
    tabletPortrait: 0,
    tabletLandscape: 0,
    desktop: 0,
}}>
          <fannypack_1.Heading use="h2">Why Pycon?</fannypack_1.Heading>
          <fannypack_1.Text>
            Lorem ipsum dolor sit amet consectetur, adipisicing elit. Sequi
            excepturi nostrum harum minima esse corrupti possimus voluptatum
            amet atque illum, maiores tempore? At in, dolorem recusandae nihil
            inventore quasi reiciendis?
          </fannypack_1.Text>
        </grigliata_1.Column>
      </grigliata_1.Row>
    </div>
  </Base>);
