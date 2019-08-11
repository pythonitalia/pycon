"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const styled_components_1 = __importDefault(require("styled-components"));
const theme_1 = require("../../config/theme");
exports.LinksWrapper = styled_components_1.default.div `
  a {
    display: block;
    color: ${theme_1.theme.palette.white};
    margin-bottom: 0.5rem;
  }
`;
