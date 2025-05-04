import QRCode from "react-qr-code";
import Balancer from "react-wrap-balancer";

import {
  BADGE_INSIDE_HEIGHT_PX,
  BADGE_INSIDE_WIDTH_PX,
  CUT_LINE_SIZE_2_PX,
  CUT_LINE_SIZE_PX,
} from "~/pages/badge";
import { ConferenceRole } from "~/types";

const BADGE_TYPE_TO_BACKGROUND_COLOR = {
  [ConferenceRole.Attendee]: "#6A80EF",
  [ConferenceRole.Speaker]: "#D75353",
  [ConferenceRole.Sponsor]: "#34B4A1",
  [ConferenceRole.Staff]: "#F17A5D",
  [ConferenceRole.Keynoter]: "#9473B0",
  [ConferenceRole.DjangoGirls]: "#EAD6CE",
};

const BADGE_TYPE_TO_COLOR = {
  [ConferenceRole.Attendee]: "#48E2B9",
  [ConferenceRole.Speaker]: "#FCE8DE",
  [ConferenceRole.Sponsor]: "#F8B03D",
  [ConferenceRole.Staff]: "#FCE8DE",
  [ConferenceRole.Keynoter]: "#F8B03D",
  [ConferenceRole.DjangoGirls]: "#F8B03D",
};

const BADGE_TYPE_TO_NAME = {
  [ConferenceRole.Attendee]: "Attendee",
  [ConferenceRole.Speaker]: "Speaker",
  [ConferenceRole.Sponsor]: "Sponsor",
  [ConferenceRole.Staff]: "Staff",
  [ConferenceRole.Keynoter]: "Keynoter",
  [ConferenceRole.DjangoGirls]: "Django Girls",
};

type Props = {
  cutLines?: boolean;
  pronouns?: string;
  tagline?: string;
  name?: string;
  role?: ConferenceRole;
  hashedTicketId?: string;
  side?: "front" | "back";
  empty?: boolean;
};

export const Badge = ({
  cutLines = true,
  name = "Kayleigh Eleanor Howe Barnett",
  pronouns = "she/her",
  tagline = "",
  role = ConferenceRole.Attendee,
  hashedTicketId = "",
  side = "front",
  empty = false,
}: Props) => {
  return (
    <div
      style={{
        backgroundColor: BADGE_TYPE_TO_BACKGROUND_COLOR[role],
        width: "100%",
        height: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        overflow: "hidden",
        position: "relative",
      }}
    >
      <div
        style={{
          width: BADGE_INSIDE_WIDTH_PX,
          height: BADGE_INSIDE_HEIGHT_PX,
          display: "flex",
          flexDirection: "column",
          textAlign: "left",
          paddingLeft: "16px",
          paddingRight: "16px",
          paddingBottom: "16px",
          position: "relative",
          zIndex: 200,
        }}
      >
        {cutLines && (
          <>
            <CutLines position="topLeft" />
            <CutLines position="topRight" />
            <CutLines position="bottomLeft" />
            <CutLines position="bottomRight" />
          </>
        )}

        {/* badge */}

        <div
          style={{
            fontSize: "10px",
            fontWeight: 600,
            color: "#000",
            background: "#fff",
            marginTop: "40px",
            marginBottom: "10px",
            opacity: pronouns ? 1 : 0,
            padding: "2px 4px",
            width: "fit-content",
            border: "1.5px solid #000",
          }}
          className="uppercase"
        >
          {pronouns || "empty"}
        </div>
        {!empty && (
          <div
            style={{
              color: "#ffffff",
              // fontSize: "40px",
              // fontSize: "32px",
              fontWeight: 600,
              lineHeight: "30px",
              wordBreak: "break-word",
            }}
            className="!text-[30px] [&>span]:text-[30px]"
          >
            <Balancer ratio={0.3}>{name}</Balancer>
          </div>
        )}
        {empty && (
          <div
            style={{
              height: "150px",
              background: "#ffffff",
            }}
          />
        )}
        <div>
          <div
            style={{
              fontSize: "26px",
              color: BADGE_TYPE_TO_COLOR[role],
              fontWeight: "bold",
              textTransform: "uppercase",
              marginTop: "8px",
              marginBottom: "8px",
            }}
          >
            {BADGE_TYPE_TO_NAME[role]}
          </div>
          <div
            style={{
              width: "90%",
              fontWeight: 400,
              color: "#ffffff",
            }}
            className="!text-[13px] [&>span]:text-[13px] badge-tagline"
          >
            <Balancer>
              <span
                style={{
                  color: BADGE_TYPE_TO_COLOR[role],
                  opacity: tagline ? 1 : 0,
                }}
                className="badge-tagline-quote"
              >
                “{" "}
              </span>
              {tagline.substring(0, 250)}
              <span
                style={{
                  color: BADGE_TYPE_TO_COLOR[role],
                  opacity: tagline ? 1 : 0,
                }}
                className="badge-tagline-quote"
              >
                {" "}
                ”
              </span>
            </Balancer>
          </div>
        </div>
        <div
          style={{
            marginTop: "auto",
            width: "100%",
            display: "flex",
            alignItems: "flex-end",
            justifyContent: "space-between",
          }}
        >
          <Cloud
            style={{
              position: "absolute",
              zIndex: 1,
              transform: "translate(40px, -30px)",
            }}
          />
          <Cloud
            style={{
              position: "absolute",
              zIndex: 1,
              transform: "translate(260px, -70px)",
            }}
          />

          {!empty && side === "front" && (
            <div className="p-[2px] bg-white border-1 z-10">
              <QRCode
                className="shrink-0"
                value={`https://pycon.it/b/${hashedTicketId}`}
                size={70}
              />
            </div>
          )}
          {(empty || side === "back") && (
            <div className="p-[2px] relative">
              <div className="w-[70px] h-[70px]" />
              <div />
            </div>
          )}

          <div
            style={{
              position: "relative",
            }}
          >
            <svg
              width="128"
              height="191"
              viewBox="0 0 128 191"
              fill="none"
              style={{
                position: "absolute",
                bottom: "34px",
              }}
            >
              {/* snake */}
              <path
                className="badge-snake a"
                d="M55.6358 73.2713V140.92C55.6358 140.922 55.6358 140.924 55.6352 140.927C55.6342 140.929 55.6332 140.931 55.6316 140.932C55.6299 140.934 55.628 140.935 55.6257 140.936C55.6238 140.936 55.6215 140.937 55.6192 140.936H44.4381C48.5978 136.539 48.5812 127.84 44.3815 123.487C40.1819 119.134 40.1672 110.349 44.3815 105.974C48.5958 101.598 48.5978 92.8426 44.3815 88.4603C40.1654 84.0776 40.1672 75.3292 44.3815 70.9485C48.5411 66.63 48.0659 58.0479 43.9977 53.6106C47.516 55.5505 50.4507 58.397 52.4973 61.8543C54.5436 65.3116 55.6273 69.2538 55.6358 73.2713Z"
                fill="#F17A5D"
              />
              <path
                className="badge-snake b"
                d="M44.3824 88.4596C48.5986 92.8459 48.5986 101.598 44.3824 105.973C40.1662 110.348 40.168 119.106 44.3824 123.487C48.5967 127.867 48.5986 136.539 44.439 140.936H33.1466C33.1443 140.936 33.1421 140.936 33.14 140.935C33.1378 140.935 33.1359 140.933 33.1343 140.932C33.1327 140.93 33.1315 140.928 33.1308 140.926C33.1301 140.924 33.1298 140.922 33.1302 140.919V72.8415C33.1302 72.8287 33.1192 72.8233 33.1064 72.8233H12.0164C12.0055 72.8233 12 72.8123 12 72.8013C12.0045 67.0948 14.2446 61.6171 18.2399 57.5425C22.2352 53.4679 27.6678 51.1208 33.3732 51.0041C37.0817 50.931 40.7448 51.8294 43.9985 53.6102C48.0667 58.0475 48.542 66.6297 44.3824 70.9482C40.168 75.3288 40.168 84.0845 44.3824 88.4596ZM29.2759 60.9223C29.2766 60.5637 29.1709 60.2131 28.9721 59.9147C28.7734 59.6163 28.4906 59.3836 28.1595 59.2461C27.8284 59.1085 27.464 59.0724 27.1123 59.1421C26.7607 59.2119 26.4376 59.3844 26.1841 59.638C25.9306 59.8915 25.758 60.2145 25.6883 60.5662C25.6185 60.9178 25.6547 61.2823 25.7922 61.6134C25.9297 61.9445 26.1624 62.2272 26.4608 62.426C26.7592 62.6247 27.1099 62.7304 27.4684 62.7297C27.9476 62.7292 28.4071 62.5386 28.7459 62.1998C29.0848 61.8609 29.2754 61.4015 29.2759 60.9223Z"
                fill="#FCE8DE"
              />
              <path
                className="badge-snake d"
                d="M27.4687 59.1129C27.8264 59.1136 28.1759 59.2204 28.4729 59.4196C28.77 59.6189 29.0013 59.9017 29.1377 60.2323C29.2741 60.563 29.3093 60.9267 29.2391 61.2774C29.1689 61.6281 28.9963 61.9502 28.7431 62.2028C28.49 62.4555 28.1676 62.6274 27.8167 62.697C27.4659 62.7665 27.1023 62.7304 26.7718 62.5934C26.4415 62.4563 26.1591 62.2245 25.9605 61.927C25.7618 61.6295 25.6558 61.2799 25.6558 60.9222C25.6558 60.6843 25.7027 60.4487 25.7939 60.229C25.885 60.0092 26.0186 59.8096 26.187 59.6416C26.3554 59.4735 26.5553 59.3403 26.7752 59.2496C26.9952 59.1589 27.2308 59.1124 27.4687 59.1129Z"
                fill="#0E1116"
              />
              <path
                className="badge-snake e"
                d="M44.439 140.936H33.1466C33.1444 140.936 33.1421 140.936 33.14 140.935C33.1378 140.935 33.1359 140.933 33.1343 140.932C33.1327 140.93 33.1315 140.928 33.1308 140.926C33.1301 140.924 33.1298 140.922 33.1302 140.919V72.8415C33.1302 72.8287 33.1192 72.8233 33.1064 72.8233H12.0164C12.0055 72.8233 12 72.8123 12 72.8013C12.0045 67.0948 14.2446 61.6171 18.2399 57.5425C22.2352 53.4679 27.6679 51.1208 33.3732 51.0041C37.0817 50.931 40.7448 51.8294 43.9986 53.6102C47.5169 55.5502 50.4516 58.3966 52.4979 61.8539C54.5445 65.3112 55.6282 69.2534 55.6363 73.271V140.919C55.6367 140.922 55.6367 140.924 55.6357 140.926C55.635 140.928 55.6337 140.93 55.6324 140.932C55.6308 140.933 55.6289 140.935 55.6266 140.935C55.6246 140.936 55.6223 140.936 55.6201 140.936H44.439Z"
                stroke="#0E1116"
                strokeWidth="1.5"
                strokeMiterlimit="1"
                strokeLinejoin="round"
              />
              <path
                className="badge-snake f"
                d="M44.3815 141C44.3997 140.976 44.4219 140.96 44.4381 140.936C48.5978 136.539 48.5812 127.84 44.3815 123.487C40.1819 119.133 40.1672 110.349 44.3815 105.973C48.5958 101.598 48.5978 92.8424 44.3815 88.4597C40.1654 84.0774 40.1672 75.3289 44.3815 70.9483C48.5411 66.6298 48.0659 58.0476 43.9977 53.6103C43.9482 53.5467 43.895 53.4857 43.8388 53.4276"
                stroke="#0E1116"
                strokeWidth="1.5"
                strokeMiterlimit="10"
                strokeLinejoin="round"
              />
              <path
                className="badge-snake g"
                d="M23.9597 72.9822V80.234L20.6317 83.5619V72.9822H27.4796V80.234L24.1516 83.5619V72.9822"
                fill="#E94135"
              />
              <path
                className="badge-snake h"
                d="M23.9597 72.9822V80.234L20.6317 83.5619V72.9822H27.4796V80.234L24.1516 83.5619V72.9822"
                stroke="#0E1116"
                strokeWidth="1.5"
                strokeMiterlimit="10"
                strokeLinejoin="round"
              />

              {/* tower left */}
              <path
                className="badge-tower-left i"
                d="M29.3318 92.4155C30.5885 93.3521 31.2151 93.8246 32.4649 94.778C32.6394 96.4801 32.802 98.1821 32.9493 99.8858C34.8986 101.078 36.8378 102.291 38.7634 103.52C47.0568 135.444 52.5762 167.869 52.7438 200.909C41.4172 200.995 30.0922 201.022 18.7656 200.967C18.7385 193.291 18.2135 185.669 17.487 178.029C16.5216 168.243 15.4699 158.573 13.6154 148.91C12.0624 140.557 10.44 132.206 8.6973 123.891C6.47854 114.685 3.91092 105.568 1 96.558L28.4579 87.9868C28.8187 89.7566 28.9931 90.6407 29.3318 92.4104V92.4155Z"
                fill="#EAD6CE"
                stroke="black"
                strokeWidth="1.5"
                strokeMiterlimit="10"
                strokeLinejoin="round"
              />
              <path
                className="badge-tower-left l"
                d="M14.8333 182.337C28.199 181.68 41.563 180.984 54.9219 180.2C55.2843 187.095 55.4452 193.986 55.4249 200.89C42.1879 201.004 28.9509 201.038 15.7139 200.951C15.7038 194.727 15.3616 188.539 14.8333 182.339V182.337Z"
                fill="#C9BFBD"
                stroke="black"
                strokeWidth="1.5"
                strokeMiterlimit="10"
                strokeLinejoin="round"
              />
              <path
                className="badge-tower-left m"
                d="M22.9579 119.851L26.9886 118.937C27.7626 122.365 28.4874 125.799 29.1936 129.242C27.5712 129.561 26.76 129.721 25.1375 130.04C24.4381 126.637 23.7217 123.24 22.9562 119.851H22.9579ZM33.3277 191.525C35.0517 191.479 36.7758 191.433 38.5015 191.384C38.6573 194.546 38.7657 197.706 38.8233 200.872C37.0942 200.878 35.365 200.882 33.6342 200.884C33.5851 197.761 33.4818 194.643 33.3277 191.523V191.525Z"
                fill="#9473B0"
                stroke="black"
                strokeWidth="1.5"
                strokeMiterlimit="10"
                strokeLinejoin="round"
              />

              {/* tower right */}
              <path
                className="badge-tower-right n"
                d="M77.761 20.5608C87.8852 24.0241 98.0093 27.4875 108.135 30.9509C87.4973 85.1773 77.6475 141.995 78.5637 199.971C67.713 199.952 56.8656 200.213 46.0149 200.195C45.2274 138.781 55.9003 77.9712 77.761 20.5608Z"
                fill="#C9BFBD"
                stroke="black"
                strokeWidth="1.5"
                strokeMiterlimit="10"
                strokeLinejoin="round"
              />
              <path
                className="badge-tower-right p"
                d="M50.9733 108.615L87.165 115.158C82.2824 143.231 80.4483 171.363 80.8937 199.837C68.5018 199.756 56.1133 200.101 43.7231 200.022C43.3386 169.36 45.7147 138.828 50.975 108.615H50.9733Z"
                fill="#EAD6CE"
                stroke="black"
                strokeWidth="1.5"
                strokeMiterlimit="10"
                strokeLinejoin="round"
              />
              <path
                className="badge-tower-right q"
                d="M80.9298 200.677C80.8485 196.558 80.7994 192.441 80.7858 188.322C82.9286 185.458 85.1061 182.619 87.318 179.807C87.3739 176.498 87.4687 173.19 87.6008 169.885C84.9232 169.663 82.244 169.463 79.5648 169.271C79.4919 171.59 79.4394 173.907 79.4022 176.225C77.6595 176.129 75.9151 176.039 74.1724 175.954C74.2402 173.609 74.3248 171.261 74.4282 168.917C71.9098 168.752 69.3915 168.591 66.8714 168.431C66.7613 170.821 66.6648 173.212 66.5818 175.604C63.8704 175.483 61.159 175.367 58.4459 175.246C58.5136 172.804 58.5949 170.364 58.6914 167.922C56.1189 167.759 53.5447 167.595 50.9721 167.425C50.8739 169.913 50.7909 172.401 50.7232 174.889C49.0245 174.806 47.3275 174.72 45.6289 174.627C45.7237 172.11 45.8338 169.597 45.9591 167.082C43.2579 166.89 40.5583 166.684 37.8605 166.464C37.6725 170.176 37.5184 173.888 37.3998 177.604C39.4541 180.969 41.5491 184.305 43.6881 187.616C43.6542 192.052 43.6711 196.485 43.7355 200.921C56.1341 200.984 68.5311 200.614 80.9298 200.679V200.677Z"
                fill="#C9BFBD"
                stroke="black"
                strokeWidth="1.5"
                strokeMiterlimit="10"
                strokeLinejoin="round"
              />
              <path
                className="badge-tower-right r"
                d="M61.6712 185.882C62.1183 185.89 62.3418 185.894 62.7889 185.902C63.5527 185.916 64.2776 186.151 64.8246 186.563C65.3717 186.974 65.6697 187.511 65.668 188.07C65.6562 192.299 65.6867 196.524 65.7544 200.751C63.4528 200.782 61.1513 200.814 58.8497 200.843C58.7836 196.553 58.7582 192.267 58.7786 187.977C58.7819 187.409 59.0885 186.874 59.6423 186.476C60.1961 186.092 60.926 185.868 61.6898 185.882H61.6729H61.6712ZM50.4902 185.653C50.9356 185.665 51.1592 185.67 51.6046 185.68C52.3667 185.699 53.0898 185.941 53.6335 186.366C54.1788 186.791 54.4752 187.342 54.4701 187.914C54.4464 192.241 54.4684 196.567 54.5328 200.894C52.238 200.917 49.9449 200.931 47.6501 200.933C47.5857 196.548 47.5688 192.163 47.5993 187.779C47.6043 187.198 47.9109 186.652 48.4647 186.248C49.0168 185.858 49.745 185.635 50.5071 185.653H50.4902ZM72.7658 186.102C73.2112 186.112 73.4348 186.117 73.8819 186.129C74.6423 186.148 75.3671 186.383 75.9125 186.79C76.4578 187.196 76.7576 187.723 76.7559 188.266C76.7559 192.399 76.7931 196.531 76.8626 200.663C74.5678 200.665 72.2747 200.68 69.9799 200.704C69.9096 196.514 69.8774 192.323 69.8833 188.133C69.885 187.581 70.1899 187.059 70.742 186.673C71.2941 186.3 72.0223 186.085 72.7827 186.104H72.7658V186.102Z"
                fill="#9473B0"
                stroke="black"
                strokeWidth="1.5"
                strokeMiterlimit="10"
                strokeLinejoin="round"
              />
              <path
                className="badge-tower-right s"
                d="M108.134 30.9508C108.755 29.2725 109.068 28.4342 109.707 26.7626C112.592 25.2981 115.487 23.8546 118.393 22.4321C119.162 20.5438 119.945 18.6606 120.741 16.7841C118.967 16.1168 117.196 15.4479 115.423 14.7806C114.793 16.3065 114.173 17.8358 113.562 19.3702C111.936 18.774 110.312 18.1779 108.686 17.5801C109.328 16.0423 109.98 14.5079 110.638 12.9786C108.296 12.0963 105.956 11.2139 103.613 10.3316C102.941 11.8795 102.279 13.4325 101.625 14.9889L94.0651 12.2148C94.7052 10.6296 95.3556 9.04616 96.0161 7.46944C93.6248 6.56846 91.2317 5.66748 88.8404 4.7665C88.1782 6.36693 87.5245 7.97074 86.8809 9.57963C85.2974 8.99874 83.7156 8.41784 82.1321 7.83695C82.8028 6.22297 83.4819 4.61239 84.1712 3.00688C82.3947 2.33792 80.6181 1.66896 78.8432 1C77.9846 3.02551 77.1412 5.0561 76.3096 7.09178C77.3342 10.1199 78.3826 13.1395 79.4546 16.1524C78.7687 17.9137 78.4283 18.796 77.7593 20.5624C87.8835 24.0258 98.0077 27.4891 108.134 30.9525V30.9508Z"
                fill="#DDD0CC"
                stroke="black"
                strokeWidth="1.5"
                strokeMiterlimit="10"
                strokeLinejoin="round"
              />
              <path
                className="badge-tower-right t"
                d="M56.9047 114.523L60.6847 115.175C60.158 118.388 59.6567 121.606 59.1825 124.827C57.6668 124.59 56.9097 124.473 55.394 124.236C55.8716 120.994 56.3763 117.756 56.9063 114.523H56.9047ZM66.5191 116.183L70.2991 116.835C69.7809 119.996 69.288 123.162 68.8207 126.331C67.3049 126.094 66.5479 125.977 65.0321 125.74C65.5029 122.549 65.9975 119.365 66.5208 116.183H66.5191ZM75.8744 117.8L79.6545 118.452C79.1447 121.563 78.6603 124.676 78.1997 127.796C76.6839 127.559 75.9269 127.442 74.4111 127.205C74.8735 124.065 75.3612 120.932 75.8761 117.8H75.8744ZM89.0928 30.5662C90.5458 31.0472 91.2724 31.2877 92.7255 31.7703C92.1666 33.2793 91.6162 34.7917 91.0759 36.3074C89.6178 35.8383 88.8895 35.6029 87.4314 35.1338C87.9767 33.6078 88.5305 32.0853 89.0928 30.5662Z"
                fill="#9473B0"
                stroke="black"
                strokeWidth="1.5"
                strokeMiterlimit="10"
                strokeLinejoin="round"
              />
            </svg>

            <img
              alt=""
              style={{
                width: "113px",
                height: "34px",
              }}
              src="https://cdn.pycon.it/conferences/pycon2025/pycon-italia-2025-logo.png"
            />
          </div>
        </div>
      </div>

      <svg
        width="331"
        height="76"
        viewBox="0 0 331 76"
        fill="none"
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          zIndex: 0,
        }}
      >
        <path
          d="M1 13.1995L9.30781 7.7411C22.1825 -0.717439 38.6375 -1.50571 52.2621 5.68349L96.6964 29.1309C109.207 35.7326 124.191 35.6415 136.62 28.8879L144.426 24.6462C157.259 17.6735 172.981 18.8343 184.65 27.6158L185.673 28.3851C198.614 38.1238 216.496 37.9088 229.2 27.8619C240.435 18.9758 255.901 17.6828 268.457 24.5798L271.599 26.3058C285.407 33.8909 302.34 32.9009 315.169 23.7582L329.986 13.1995V75.5011H1V13.1995Z"
          fill="#47E2B9"
        />
        <path
          d="M1 13.1995L9.30781 7.7411C22.1825 -0.717439 38.6375 -1.50571 52.2621 5.68349L96.6964 29.1309C109.207 35.7326 124.191 35.6415 136.62 28.8879L144.426 24.6462C157.259 17.6735 172.981 18.8343 184.65 27.6158L185.673 28.3851C198.614 38.1238 216.496 37.9088 229.2 27.8619C240.435 18.9758 255.901 17.6828 268.457 24.5798L271.599 26.3058C285.407 33.8909 302.34 32.9009 315.169 23.7582L329.986 13.1995"
          stroke="#0E1116"
          strokeWidth="1.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    </div>
  );
};

const CutLines = ({
  position,
}: {
  position: "topRight" | "topLeft" | "bottomRight" | "bottomLeft";
}) => {
  let container = {};
  let line1 = {};
  let line2 = {};

  switch (position) {
    case "topLeft":
      container = {
        top: 0,
        left: 0,
      };
      line1 = {
        width: CUT_LINE_SIZE_PX,
        height: CUT_LINE_SIZE_2_PX,
        top: 0,
        left: 0,
        transform: "translateX(-100%)",
      };
      line2 = {
        width: CUT_LINE_SIZE_2_PX,
        height: CUT_LINE_SIZE_PX,

        transform: "translateY(-100%)",
        top: 0,
        left: 0,
      };
      break;
    case "bottomLeft":
      container = {
        bottom: 0,
        left: 0,
      };
      line1 = {
        width: CUT_LINE_SIZE_PX,
        height: CUT_LINE_SIZE_2_PX,
        bottom: 0,
        left: 0,
        transform: "translateX(-100%)",
      };
      line2 = {
        width: CUT_LINE_SIZE_2_PX,
        height: CUT_LINE_SIZE_PX,

        transform: "translateY(100%)",
        bottom: 0,
        left: 0,
      };
      break;
    case "topRight":
      container = {
        top: 0,
        right: 0,
      };
      line1 = {
        width: CUT_LINE_SIZE_2_PX,
        height: CUT_LINE_SIZE_PX,
        top: 0,
        left: 0,
        transform: "translateY(-100%) translateX(-100%)",
      };
      line2 = {
        width: CUT_LINE_SIZE_PX,
        height: CUT_LINE_SIZE_2_PX,

        transform: "translateX(100%)",
        top: 0,
        right: 0,
      };
      break;
    case "bottomRight":
      container = {
        bottom: 0,
        right: 0,
      };
      line1 = {
        width: CUT_LINE_SIZE_2_PX,
        height: CUT_LINE_SIZE_PX,
        bottom: 0,
        left: 0,
        transform: "translateY(100%) translateX(-100%)",
      };
      line2 = {
        width: CUT_LINE_SIZE_PX,
        height: CUT_LINE_SIZE_2_PX,

        transform: "translateX(100%)",
        bottom: 0,
        right: 0,
      };
      break;
  }

  return (
    <div
      style={{
        position: "absolute",
        display: "flex",
        zIndex: 100,
        ...container,
      }}
    >
      {/* cut lines */}
      <div
        style={{
          position: "absolute",
          backgroundColor: "#ffffff",
          display: "flex",
          ...line1,
        }}
      />
      <div
        style={{
          position: "absolute",
          backgroundColor: "#ffffff",
          display: "flex",
          ...line2,
        }}
      />
    </div>
  );
};

const Cloud = ({ style }) => (
  <svg width="66" height="22" viewBox="0 0 66 22" fill="none" style={style}>
    <path
      d="M64.4269 21C64.3838 19.2087 63.8822 17.4584 62.9706 15.9161C62.0585 14.3737 60.7663 13.0909 59.2177 12.19C57.6687 11.2891 55.9149 10.8001 54.1232 10.7698C52.3319 10.7396 50.5623 11.169 48.9839 12.017C48.0483 8.97687 46.2062 6.29515 43.704 4.33102C41.2022 2.36688 38.1595 1.21409 34.9842 1.02702C31.8089 0.839957 28.6521 1.62755 25.9368 3.28433C23.2214 4.94112 21.0771 7.38796 19.7909 10.2972C17.9283 9.09962 15.7747 8.43179 13.5613 8.36537C11.3478 8.29892 9.15802 8.83642 7.22689 9.92019C5.29578 11.004 3.69617 12.5931 2.59976 14.517C1.50333 16.441 0.951466 18.6272 1.00335 20.841L64.4269 21Z"
      fill="white"
      stroke="#0E1116"
      strokeWidth="1.5"
      strokeMiterlimit="10"
      strokeLinejoin="round"
    />
  </svg>
);
