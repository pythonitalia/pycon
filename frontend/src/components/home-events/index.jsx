"use strict";
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
    result["default"] = mod;
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = __importStar(require("react"));
const grigliata_1 = require("grigliata");
const styled_components_1 = __importDefault(require("styled-components"));
const spacing_1 = require("../../config/spacing");
const theme_1 = require("../../config/theme");
const section_title_1 = require("../section-title");
const Wrapper = styled_components_1.default.div `
    @media (min-width: 1024px) {
      margin-top: 2rem;
    }
    p {
      margin-top: 0;
    }
  `, EventsContainer = styled_components_1.default.div `
    overflow-x: scroll;
    width: 100%;
    white-space: nowrap;
    &:hover {
      cursor: pointer;
    }
    -ms-overflow-style: none; // IE 10+
    scrollbar-width: none; // Firefox
    &::-webkit-scrollbar {
      display: none; // Safari and Chrome
    }

    .event_card {
      display: inline-block;
      margin-right: 16px;
      padding: 8px;
      color: ${theme_1.theme.palette.white};
      &:first-child {
        margin-left: 2.5rem;
        @media (min-width: 1024px) {
          margin-left: 15rem;
        }
      }
      .event_card_content {
        position: absolute;
        left: 16px;
        bottom: 16px;
      }
      .event_card_content__title {
        color: ${theme_1.theme.palette.white};
        margin: 0;
      }
      .event_card_content__subtitle {
        color: ${theme_1.theme.palette.white};
        margin: 0;
      }
    }
  `, EventCard = styled_components_1.default.div `
    background: linear-gradient(
      29.43deg,
      #0c67ff 0%,
      rgba(12, 103, 255, 0.0001) 125.98%
    );
    box-shadow: 0px 0px 1px rgba(0, 0, 0, 0.08);
    border-radius: 8px;
    height: 200px;
    width: 300px;
    position: relative;
  `, EventCardContent = () => (<div className="event_card_content">
      <p className="event_card_content__title">h. 21:00 Pub James Joyce</p>
      <p className="event_card_content__subtitle">PyBirra</p>
    </div>);
exports.Events = () => {
    react_1.useEffect(() => {
        const slider = document.querySelector(".events");
        let isDown = false, startX = 0, scrollLeft = 0;
        if (slider) {
            slider.addEventListener("mousedown", (e) => {
                isDown = true;
                slider.classList.add("active");
                startX = e.pageX - slider.offsetLeft;
                scrollLeft = slider.scrollLeft;
            });
            slider.addEventListener("mouseleave", () => {
                isDown = false;
                slider.classList.remove("active");
            });
            slider.addEventListener("mouseup", () => {
                isDown = false;
                slider.classList.remove("active");
            });
            slider.addEventListener("mousemove", (e) => {
                if (!isDown) {
                    return null;
                }
                e.preventDefault();
                const x = e.pageX - slider.offsetLeft, walk = (x - startX) * 1.5;
                slider.scrollLeft = scrollLeft - walk;
            });
        }
        return () => {
            // return null
        };
    });
    return (<Wrapper>
      <grigliata_1.Row paddingLeft={spacing_1.STANDARD_ROW_PADDING} paddingRight={spacing_1.STANDARD_ROW_PADDING}>
        <grigliata_1.Column columnWidth={{
        mobile: 12,
        tabletPortrait: 12,
        tabletLandscape: 12,
        desktop: 12,
    }}>
          <section_title_1.SectionTitle>EVENTS</section_title_1.SectionTitle>
        </grigliata_1.Column>
      </grigliata_1.Row>

      <grigliata_1.Row marginTop={{
        desktop: -4,
        tabletLandscape: -3,
        tabletPortrait: 0,
        mobile: 0,
    }} paddingLeft={spacing_1.STANDARD_ROW_PADDING} paddingRight={spacing_1.STANDARD_ROW_PADDING}>
        <grigliata_1.Column columnWidth={{
        mobile: 12,
        tabletPortrait: 6,
        tabletLandscape: 6,
        desktop: 6,
    }}>
          <p>
            Lorem ipsum, dolor sit amet consectetur adipisicing elit maxime
            reiciendis a consectetur nisi temporibus!
          </p>
        </grigliata_1.Column>
      </grigliata_1.Row>

      <grigliata_1.Row marginTop={{
        desktop: 2,
        tabletLandscape: 2,
        tabletPortrait: 0,
        mobile: 0,
    }}>
        <EventsContainer className="events">
          {[1, 2, 3, 4, 5, 6, 7].map((o, i) => (<EventCard key={i} className="event_card">
              <EventCardContent />
            </EventCard>))}
        </EventsContainer>
      </grigliata_1.Row>
    </Wrapper>);
};
