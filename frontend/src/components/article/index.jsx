"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = __importDefault(require("react"));
const grigliata_1 = require("grigliata");
const styled_components_1 = __importDefault(require("styled-components"));
const hero_1 = require("../hero");
const title_1 = require("./title");
const Wrapper = styled_components_1.default.div `
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

  ${title_1.ArticleTitle} {
    margin-bottom: 0.3em;

    @media (min-width: 1024px) {
      font-size: 42px;
      line-height: 32px;
    }
    @media (min-width: 1366px) {
      font-size: 90px;
      line-height: 72px;
    }
  }

  p {
    margin-top: 0;
  }
`;
exports.Article = props => (<Wrapper>
    <hero_1.Hero title={props.title} backgroundImage={props.hero}>
      {props.description && <p> {props.description} </p>}
    </hero_1.Hero>
    <grigliata_1.Row marginTop={{
    mobile: 2,
    tabletPortrait: 2,
    tabletLandscape: 2,
    desktop: 2,
}} paddingLeft={{
    mobile: 2,
    tabletPortrait: 2,
    tabletLandscape: 2,
    desktop: 2,
}} paddingRight={{
    mobile: 2,
    tabletPortrait: 2,
    tabletLandscape: 2,
    desktop: 2,
}}>
      <div className="content">{props.children}</div>
    </grigliata_1.Row>
  </Wrapper>);
