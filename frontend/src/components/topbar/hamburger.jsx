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
const styled_components_1 = __importStar(require("styled-components"));
const theme_1 = require("../../config/theme");
const Draw = styled_components_1.default.div `
  width: 40px;
  height: 24px;
  margin-right: 0.5rem;
  position: relative;
  transform: rotate(0deg);
  transition: 0.5s ease-in-out transform;
  cursor: pointer;

  span {
    display: block;
    position: absolute;
    height: 4px;
    width: 100%;
    background: ${theme_1.theme.palette.primary};
    border-radius: 9px;
    opacity: 1;
    transform: rotate(0deg);
    transition: 0.25s ease-in-out transform;
  }

  span:nth-child(1) {
    top: 0px;
  }

  span:nth-child(2) {
    top: 10px;
  }

  span:nth-child(3) {
    top: 20px;
  }

  ${props => props.open &&
    styled_components_1.css `
      span:nth-child(1) {
        top: 10px;
        transform: rotate(135deg);
      }
      span:nth-child(2) {
        opacity: 0;
        left: -60px;
      }
      span:nth-child(3) {
        top: 10px;
        transform: rotate(-135deg);
      }
      span {
        background: ${theme_1.theme.palette.white};
        left: -4px;
      }
    `}
`;
exports.Hamburger = ({ open }) => (<div>
    <Draw open={open}>
      <span />
      <span />
      <span />
    </Draw>
  </div>);
