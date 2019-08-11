"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = __importDefault(require("react"));
const grigliata_1 = require("grigliata");
const styled_components_1 = __importDefault(require("styled-components"));
const spacing_1 = require("../../config/spacing");
const theme_1 = require("../../config/theme");
const Wrapper = styled_components_1.default.div `
    div[class^="columns__CustomColumns"] {
      display: block;

      @media (min-width: 992px) {
        display: flex;
      }
    }
  `, Headings = styled_components_1.default.div `
    border-top: 1px solid ${theme_1.theme.palette.white};
    padding-top: 0px;
    margin: 0.5rem 0;

    @media (min-width: 992px) {
      margin: 5rem auto;
    }
    p {
      margin-bottom: 0;
      margin-top: 0.5rem;

      @media (min-width: 992px) {
        margin-top: 1rem;
      }
    }
  `, Base = ({ ...props }) => (<div {...props}>
      <Wrapper className="expanded_menu">
        <grigliata_1.Row paddingLeft={spacing_1.STANDARD_ROW_PADDING} paddingRight={spacing_1.STANDARD_ROW_PADDING}>
          <grigliata_1.Column columnWidth={{
    mobile: 12,
    tabletPortrait: 6,
    tabletLandscape: 4,
    desktop: 4,
}}>
            <Headings>
              <h3>Heading</h3>
              <p>
                <a href="#">Linkoone</a>
              </p>
              <p>
                <a href="#">Link</a>
              </p>
              <p>
                <a href="#">Linkoone</a>
              </p>
            </Headings>
          </grigliata_1.Column>
          <grigliata_1.Column columnWidth={{
    mobile: 12,
    tabletPortrait: 6,
    tabletLandscape: 4,
    desktop: 4,
}}>
            <Headings>
              <h3>Heading</h3>
              <p>
                <a href="#">Associazione</a>
              </p>
              <p>
                <a href="#">Linkoone</a>
              </p>
              <p>
                <a href="#">Linkoone</a>
              </p>
              <p>
                <a href="#">Linkettonino</a>
              </p>
              <p>
                <a href="#">Link hello</a>
              </p>
            </Headings>
          </grigliata_1.Column>
          <grigliata_1.Column columnWidth={{
    mobile: 12,
    tabletPortrait: 6,
    tabletLandscape: 4,
    desktop: 4,
}}>
            <Headings>
              <h3>Heading</h3>
              <p>
                <a href="#">Linkoone</a>
              </p>
              <p>
                <a href="#">Link for try</a>
              </p>
              <p>
                <a href="#">Link</a>
              </p>
              <p>
                <a href="#">Linkoone</a>
              </p>
            </Headings>
          </grigliata_1.Column>
        </grigliata_1.Row>
      </Wrapper>
    </div>);
exports.ExpandedMenu = styled_components_1.default(Base) `
  position: fixed;
  width: 100%;
  top: 80px;
  left: 0;
  background-color: ${theme_1.theme.palette.primary};
  color: ${theme_1.theme.palette.white};

  .expanded_menu {
    overflow-y: scroll;
    height: calc(100% - 80px);
  }
`;
