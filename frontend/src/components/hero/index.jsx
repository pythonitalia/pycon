"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = __importDefault(require("react"));
const fannypack_1 = require("fannypack");
const gatsby_image_1 = __importDefault(require("gatsby-image"));
const grigliata_1 = require("grigliata");
const styled_components_1 = __importDefault(require("styled-components"));
const spacing_1 = require("../../config/spacing");
const Wrapper = styled_components_1.default.div `
  position: relative;
  padding: 2.5rem 0 0 0;
  color: ${fannypack_1.theme("palette.white")};

  &::before {
    content: "";
    display: block;
    background: ${fannypack_1.theme("palette.primary")};
    top: 0;
    bottom: 0;
    left: 1rem;
    right: 1rem;
    position: absolute;
    z-index: 0;
  }

  .content {
    position: relative;
    z-index: 1;
  }

  img {
    width: 100%;
    height: auto;
  }

  header {
    position: relative;
  }

  h1 {
    position: absolute;
    bottom: 0;
    left: 16px;
    margin: 0;
    color: white;
    font-size: 35px;
    line-height: 25px;
    @media (min-width: 768px) {
      font-size: 55px;
      line-height: 45px;
    }
    @media (min-width: 1024px) {
      font-size: 92px;
      line-height: 70px;
    }
    @media (min-width: 1366px) {
      font-size: 120px;
      line-height: 92px;
    }
  }

  p {
    margin-top: 0;
  }
`;
exports.Hero = props => (<Wrapper>
    <div className="content">
      <header>
        <div style={{ position: "relative" }}>
          <gatsby_image_1.default {...props.backgroundImage}/>
          <h1>{props.title}</h1>
        </div>
      </header>

      <grigliata_1.Row paddingLeft={spacing_1.STANDARD_ROW_PADDING} paddingRight={spacing_1.STANDARD_ROW_PADDING}>
        <grigliata_1.Column paddingTop={{
    mobile: 3,
    tabletPortrait: 3,
    tabletLandscape: 3,
    desktop: 3,
}} paddingBottom={{
    mobile: 3,
    tabletPortrait: 3,
    tabletLandscape: 3,
    desktop: 3,
}} paddingLeft={{
    mobile: 3,
    tabletPortrait: 3,
    tabletLandscape: 3,
    desktop: 3,
}} paddingRight={{
    mobile: 3,
    tabletPortrait: 3,
    tabletLandscape: 3,
    desktop: 3,
}} columnWidth={{
    mobile: 12,
    tabletPortrait: 12,
    tabletLandscape: 12,
    desktop: 12,
}}>
          {props.children}
        </grigliata_1.Column>
      </grigliata_1.Row>
    </div>
  </Wrapper>);
