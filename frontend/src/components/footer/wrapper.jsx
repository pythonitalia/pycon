"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const styled_components_1 = __importDefault(require("styled-components"));
const theme_1 = require("../../config/theme");
exports.Wrapper = styled_components_1.default.div `
  margin-top: 3rem;
  background-color: ${theme_1.theme.palette.primary};
  color: ${theme_1.theme.palette.white};
  position: relative;
  display: block;
  padding-bottom: 0.5rem;

  h3 {
    margin-top: 0;
  }

  .margin-mobile-0-r {
    margin-bottom: 4rem;
  }

  @media only screen and (min-width: 578px) {
    margin-top: 3rem;

    .margin-mobile-0-r,
    .margin-mobile-0-l {
      margin: 0;
      margin-bottom: 4rem;
    }
  }
  @media only screen and (min-width: 992px) {
    margin-top: 8rem;
    .margin-mobile-0-r {
      margin-right: 4rem;
      margin-bottom: 0;
    }
    .margin-mobile-0-l {
      margin-left: 4rem;
      margin-bottom: 0;
    }
  }
`;
