"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
    result["default"] = mod;
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = __importDefault(require("react"));
const fannypack_1 = require("fannypack");
const grigliata_1 = require("grigliata");
const styled_components_1 = __importStar(require("styled-components"));
const spacing_1 = require("../../config/spacing");
const theme_1 = require("../../config/theme");
const use_toggle_1 = require("../../helpers/use-toggle");
const button_1 = require("../button");
const expanded_menu_1 = require("./expanded-menu");
const hamburger_1 = require("./hamburger");
const LinkContainer = styled_components_1.default.div `
    display: flex;
    align-items: center;
    justify-content: flex-end;
    height: 100%;
    display: none;
    @media (min-width: 992px) {
      display: flex;
    }
    a {
      margin-right: 2rem;
      text-decoration: none;
      &:last-child {
        margin-right: 0;
      }
    }
  `, LogoContainer = styled_components_1.default.div `
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    height: 100%;
    align-items: center;
    font-family: Rubik;
    font-style: normal;
    font-weight: normal;
    font-size: 24px;
    justify-content: center;
    ${props => props.open &&
    styled_components_1.css `
        color: ${theme_1.theme.palette.white};
      `}
  `, MenuContainer = styled_components_1.default.div `
    display: flex;
    align-items: center;
    height: 100%;

    a {
      text-decoration: none;
      display: flex;
      align-items: center;
      outline: none;
      transition: 0.25s ease-in-out;
      .label {
        display: none;
        @media (min-width: 992px) {
          display: inline-block;
        }
      }
      &:hover,
      &:focus {
        ${props => props.open &&
    styled_components_1.css `
            color: ${theme_1.theme.palette.white};
          `}
        span, span:hover, span:focus {
          background: ${theme_1.theme.palette.primary};
          ${props => props.open
    ? styled_components_1.css `
                  background: ${theme_1.theme.palette.white};
                `
    : styled_components_1.css `
                  background: ${theme_1.theme.palette.primary};
                `}}
        }
      }
    }
  `, Wrapper = styled_components_1.default.div `
    height: 80px;
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    z-index: 10;
    background-color: ${theme_1.theme.palette.white};
    ${props => props.open &&
    styled_components_1.css `
        background-color: ${theme_1.theme.palette.primary};
        a {
          color: ${theme_1.theme.palette.white};
        }
      `}
    > div,
  > div > div {
      height: 100%;
      margin-top: 0;
      margin-bottom: 0;
    }
  `;
exports.Topbar = () => {
    const [isMenuOpen, toggleMenu] = use_toggle_1.useToggle(false);
    return (<Wrapper open={isMenuOpen}>
      <LogoContainer open={isMenuOpen}>PyCon Italia</LogoContainer>

      <grigliata_1.Row paddingLeft={spacing_1.STANDARD_ROW_PADDING} paddingRight={spacing_1.STANDARD_ROW_PADDING}>
        <grigliata_1.Column columnWidth={{
        mobile: 3,
        tabletPortrait: 6,
        tabletLandscape: 6,
        desktop: 6,
    }}>
          <MenuContainer open={isMenuOpen}>
            <fannypack_1.Link href="#" onClick={e => {
        e.preventDefault();
        toggleMenu();
    }}>
              <hamburger_1.Hamburger open={isMenuOpen}/>{" "}
              <span className="label">Menu</span>
            </fannypack_1.Link>
          </MenuContainer>
        </grigliata_1.Column>
        <grigliata_1.Column columnWidth={{
        mobile: 0,
        tabletPortrait: 6,
        tabletLandscape: 6,
        desktop: 6,
    }}>
          <LinkContainer>
            <fannypack_1.Link href="#">Login</fannypack_1.Link>
            <fannypack_1.Link href="#">Schedule</fannypack_1.Link>
            <button_1.Button palette={isMenuOpen ? "white" : "primary"}>
              GET YOUR TICKET
            </button_1.Button>
          </LinkContainer>
        </grigliata_1.Column>
      </grigliata_1.Row>

      {isMenuOpen && <expanded_menu_1.ExpandedMenu />}
    </Wrapper>);
};
