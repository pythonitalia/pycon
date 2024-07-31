import {
  Button,
  Grid,
  GridColumn,
  Heading,
  Section,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import {
  SnakeInDragon,
  SnakeInDragonInverted,
} from "@python-italia/pycon-styleguide/illustrations";
import { format } from "date-fns";
import { FormattedMessage } from "react-intl";

import { useCurrentLanguage } from "~/locale/context";
import type { Cta } from "~/types";

import { createHref } from "../link";

type Props = {
  guestName: string;
  guestJobTitle: string;
  guestPhoto: string;
  eventDate: string;
  cta: Cta | null;
};

export const SpecialGuestSection = ({
  guestName,
  guestJobTitle,
  eventDate,
  guestPhoto,
  cta,
}: Props) => {
  const language = useCurrentLanguage();
  return (
    <div className="relative bg-[#151C28] overflow-hidden">
      <BgIllustration />

      <div>
        <Section spacingSize="3xl">
          <Grid cols={12}>
            <GridColumn colSpan={7}>
              <Heading size="display2" color="milk">
                <FormattedMessage id="specialGuest.title" />
              </Heading>
              <Spacer size="xl" showOnlyOn="desktop" />
              <Spacer size="medium" showOnlyOn="mobile" />
              <Spacer size="medium" showOnlyOn="tablet" />
              <div className="hidden lg:block">
                <SnakeInDragon />
              </div>
              <div className="lg:hidden flex items-end justify-end">
                <SnakeInDragonInverted />
              </div>
            </GridColumn>
            <GridColumn
              colSpan={4}
              className="flex flex-col items-center justify-center z-10"
            >
              <Spacer size="medium" showOnlyOn="mobile" />
              <Spacer size="medium" showOnlyOn="tablet" />
              <img
                alt="Special guest"
                src={guestPhoto}
                className="w-72 aspect-square object-cover border"
              />
              <Spacer size="medium" />
              <Heading size={1} color="milk" align="center">
                {guestName}
              </Heading>
              <Heading size={3} align="center" color="milk">
                {guestJobTitle}
              </Heading>
              <Spacer size="medium" />
              <Text size="label1" color="coral">
                {format(
                  new Date(`${eventDate}T00:00:00`),
                  "EEEE - d MMMM yyyy",
                )}
              </Text>

              {cta && (
                <>
                  <Spacer size="medium" />
                  <Button
                    variant="secondary"
                    href={createHref({
                      path: cta.link,
                      locale: language,
                    })}
                  >
                    {cta.label}
                  </Button>
                </>
              )}
            </GridColumn>
          </Grid>
        </Section>
      </div>
    </div>
  );
};

const BgIllustration = () => (
  <svg
    aria-label="Special guest background"
    role="img"
    width="100%"
    height="1024"
    fill="none"
    className="absolute top-0 w-full h-full"
  >
    <defs>
      <pattern
        id="specialGuestBg"
        patternUnits="userSpaceOnUse"
        width="1440"
        height="1024"
      >
        <path
          opacity="0.4"
          d="M480.526 350.398C480.61 349.248 482.252 349.129 482.5 350.255L485.037 361.746C485.132 362.178 485.5 362.496 485.941 362.528L497.678 363.379C498.828 363.463 498.947 365.104 497.821 365.353L486.33 367.889C485.898 367.985 485.58 368.352 485.548 368.794L484.697 380.531C484.613 381.681 482.971 381.8 482.723 380.674L480.186 369.183C480.091 368.751 479.723 368.433 479.282 368.401L467.545 367.55C466.395 367.466 466.276 365.824 467.402 365.576L478.893 363.039C479.325 362.944 479.643 362.576 479.675 362.135L480.526 350.398Z"
          fill="#FCE8DE"
        />
        <path
          d="M239.953 320.565C240.61 319.618 242.084 320.351 241.724 321.447L240.046 326.567C239.908 326.987 240.063 327.448 240.426 327.7L244.854 330.771C245.802 331.428 245.069 332.902 243.973 332.543L238.852 330.865C238.432 330.727 237.971 330.882 237.719 331.245L234.648 335.673C233.991 336.621 232.517 335.887 232.876 334.792L234.555 329.671C234.692 329.251 234.538 328.79 234.174 328.538L229.746 325.467C228.799 324.81 229.532 323.336 230.628 323.695L235.748 325.374C236.169 325.511 236.629 325.357 236.882 324.993L239.953 320.565Z"
          fill="#FCE8DE"
        />
        <path
          d="M22.95 292.313C23.0334 291.163 24.6754 291.044 24.9239 292.17L26.3394 298.583C26.4347 299.015 26.8025 299.333 27.2436 299.365L33.7938 299.84C34.9438 299.923 35.0629 301.565 33.937 301.814L27.5239 303.229C27.0921 303.325 26.7741 303.692 26.7421 304.133L26.267 310.684C26.1836 311.834 24.5417 311.953 24.2932 310.827L22.8776 304.414C22.7823 303.982 22.4146 303.664 21.9735 303.632L15.4232 303.157C14.2732 303.073 14.1541 301.431 15.28 301.183L21.6931 299.767C22.125 299.672 22.4429 299.304 22.4749 298.863L22.95 292.313Z"
          fill="#FCE8DE"
        />
        <path
          d="M759.961 219.22C760.52 218.211 762.06 218.792 761.813 219.918L760.541 225.727C760.446 226.159 760.646 226.602 761.033 226.816L766.237 229.694C767.245 230.253 766.665 231.793 765.538 231.546L759.73 230.273C759.298 230.179 758.855 230.379 758.641 230.766L755.762 235.969C755.204 236.978 753.663 236.398 753.91 235.271L755.183 229.463C755.277 229.031 755.077 228.588 754.69 228.374L749.487 225.495C748.478 224.937 749.059 223.396 750.185 223.643L755.994 224.916C756.426 225.01 756.869 224.81 757.083 224.423L759.961 219.22Z"
          fill="#FCE8DE"
        />
        <path
          d="M594.345 278.25C594.781 277.182 596.379 277.578 596.266 278.726L595.74 284.08C595.696 284.52 595.947 284.936 596.357 285.103L601.338 287.137C602.405 287.572 602.009 289.17 600.862 289.058L595.508 288.532C595.068 288.488 594.651 288.739 594.484 289.149L592.451 294.129C592.015 295.197 590.417 294.801 590.53 293.654L591.056 288.3C591.099 287.86 590.848 287.443 590.439 287.276L585.458 285.243C584.391 284.807 584.786 283.209 585.934 283.322L591.288 283.848C591.728 283.891 592.144 283.64 592.311 283.231L594.345 278.25Z"
          fill="#FCE8DE"
        />
        <path
          d="M1225.31 178.297C1225.75 177.229 1227.35 177.625 1227.23 178.773L1226.71 184.127C1226.67 184.567 1226.92 184.983 1227.33 185.15L1232.31 187.183C1233.37 187.619 1232.98 189.217 1231.83 189.104L1226.48 188.578C1226.04 188.535 1225.62 188.786 1225.45 189.196L1223.42 194.176C1222.98 195.244 1221.39 194.848 1221.5 193.701L1222.02 188.347C1222.07 187.906 1221.82 187.49 1221.41 187.323L1216.43 185.29C1215.36 184.854 1215.76 183.256 1216.9 183.369L1222.26 183.895C1222.7 183.938 1223.11 183.687 1223.28 183.277L1225.31 178.297Z"
          fill="#FCE8DE"
        />
        <path
          opacity="0.2"
          d="M181.014 1.02803C181.606 -0.0143999 183.196 0.677276 182.837 1.82106L177.217 19.7404C177.014 20.3874 177.5 21.0446 178.178 21.0397L196.958 20.9041C198.157 20.8955 198.353 22.6189 197.183 22.8801L178.854 26.9722C178.192 27.1199 177.866 27.8696 178.21 28.4544L187.717 44.6503C188.324 45.6841 186.929 46.7158 186.118 45.8332L173.41 32.0059C172.951 31.5067 172.139 31.5992 171.804 32.1889L162.531 48.5203C161.94 49.5628 160.349 48.8711 160.708 47.7273L166.328 29.8079C166.531 29.1609 166.045 28.5038 165.367 28.5087L146.587 28.6442C145.389 28.6529 145.192 26.9295 146.362 26.6683L164.691 22.5762C165.353 22.4284 165.679 21.6788 165.336 21.094L155.828 4.89807C155.222 3.86429 156.616 2.83256 157.427 3.71515L170.135 17.5424C170.594 18.0417 171.406 17.9492 171.741 17.3595L181.014 1.02803Z"
          fill="#FCE8DE"
        />
        <path
          d="M1252.97 257.477C1253.56 256.435 1255.15 257.126 1254.79 258.27L1249.17 276.19C1248.97 276.837 1249.45 277.494 1250.13 277.489L1268.91 277.353C1270.11 277.345 1270.31 279.068 1269.14 279.329L1250.81 283.421C1250.15 283.569 1249.82 284.319 1250.16 284.904L1259.67 301.1C1260.28 302.133 1258.88 303.165 1258.07 302.282L1245.36 288.455C1244.9 287.956 1244.09 288.048 1243.76 288.638L1234.48 304.97C1233.89 306.012 1232.3 305.32 1232.66 304.177L1238.28 286.257C1238.48 285.61 1238 284.953 1237.32 284.958L1218.54 285.093C1217.34 285.102 1217.15 283.379 1218.32 283.117L1236.64 279.025C1237.31 278.878 1237.63 278.128 1237.29 277.543L1227.78 261.347C1227.17 260.314 1228.57 259.282 1229.38 260.164L1242.09 273.992C1242.55 274.491 1243.36 274.398 1243.69 273.809L1252.97 257.477Z"
          fill="#FCE8DE"
        />
        <path
          d="M1045.8 1.00121C1046.39 -0.0412183 1047.98 0.650448 1047.62 1.79423L1046.48 5.44015C1046.28 6.08718 1046.76 6.7443 1047.44 6.73941L1051.26 6.71183C1052.46 6.70318 1052.66 8.42659 1051.49 8.68778L1047.76 9.52037C1047.1 9.66812 1046.77 10.4178 1047.11 11.0026L1049.05 14.2978C1049.65 15.3316 1048.26 16.3634 1047.45 15.4808L1044.86 12.6674C1044.4 12.1682 1043.59 12.2607 1043.26 12.8504L1041.37 16.1732C1040.78 17.2156 1039.19 16.524 1039.55 15.3802L1040.69 11.7343C1040.89 11.0872 1040.41 10.4301 1039.73 10.435L1035.91 10.4626C1034.71 10.4712 1034.51 8.74784 1035.68 8.48665L1039.41 7.65406C1040.07 7.50631 1040.4 6.75665 1040.06 6.17185L1038.12 2.87659C1037.52 1.84281 1038.91 0.811075 1039.72 1.69366L1042.31 4.507C1042.77 5.00627 1043.58 4.91374 1043.91 4.32405L1045.8 1.00121Z"
          fill="#FCE8DE"
        />
        <path
          opacity="0.4"
          d="M10.9864 34.9387C11.5782 33.8963 13.1689 34.5879 12.8101 35.7317L11.6665 39.3777C11.4636 40.0247 11.9498 40.6818 12.6279 40.6769L16.4489 40.6493C17.6476 40.6407 17.8439 42.3641 16.674 42.6253L12.9447 43.4579C12.2829 43.6056 11.957 44.3553 12.3002 44.9401L14.2346 48.2353C14.8414 49.2691 13.4471 50.3009 12.6359 49.4183L10.0503 46.6049C9.59141 46.1057 8.7792 46.1982 8.44439 46.7879L6.55779 50.1107C5.96594 51.1531 4.37526 50.4615 4.73402 49.3177L5.87761 45.6718C6.08055 45.0247 5.59432 44.3676 4.91622 44.3725L1.09526 44.4001C-0.103436 44.4087 -0.299776 42.6853 0.870151 42.4241L4.5994 41.5916C5.26122 41.4438 5.58719 40.6941 5.2439 40.1094L3.30954 36.8141C2.7027 35.7803 4.09704 34.7486 4.90821 35.6312L7.49387 38.4445C7.95274 38.9438 8.76495 38.8512 9.09975 38.2615L10.9864 34.9387Z"
          fill="#FCE8DE"
        />
        <path
          d="M1226.51 740.213C1227.01 739.328 1228.36 739.915 1228.06 740.886V740.886C1227.88 741.436 1228.3 741.994 1228.87 741.99V741.99C1229.89 741.982 1230.06 743.446 1229.06 743.667V743.667C1228.5 743.793 1228.22 744.429 1228.52 744.926V744.926C1229.03 745.804 1227.85 746.68 1227.16 745.93V745.93C1226.77 745.506 1226.08 745.585 1225.8 746.086V746.086C1225.29 746.971 1223.94 746.383 1224.25 745.412V745.412C1224.42 744.863 1224.01 744.305 1223.43 744.309V744.309C1222.41 744.316 1222.25 742.853 1223.24 742.631V742.631C1223.8 742.506 1224.08 741.869 1223.79 741.373V741.373C1223.27 740.495 1224.46 739.619 1225.14 740.369V740.369C1225.53 740.792 1226.22 740.714 1226.51 740.213V740.213Z"
          fill="#FCE8DE"
        />
        <path
          d="M665.726 367.78C666.229 366.894 667.58 367.482 667.275 368.453V368.453C667.103 369.002 667.515 369.56 668.091 369.556V369.556C669.109 369.549 669.276 371.012 668.282 371.234V371.234C667.72 371.359 667.444 371.996 667.735 372.492V372.492C668.25 373.37 667.066 374.246 666.378 373.497V373.497C665.988 373.073 665.298 373.151 665.014 373.652V373.652C664.512 374.537 663.161 373.95 663.466 372.979V372.979C663.638 372.429 663.225 371.871 662.649 371.876V371.876C661.632 371.883 661.465 370.42 662.458 370.198V370.198C663.02 370.072 663.297 369.436 663.005 368.939V368.939C662.49 368.062 663.674 367.186 664.363 367.935V367.935C664.752 368.359 665.442 368.28 665.726 367.78V367.78Z"
          fill="#FCE8DE"
        />
        <path
          d="M1232.21 401.94C1232.71 401.055 1234.06 401.642 1233.76 402.613V402.613C1233.59 403.162 1234 403.72 1234.58 403.716V403.716C1235.59 403.709 1235.76 405.172 1234.77 405.394V405.394C1234.2 405.519 1233.93 406.156 1234.22 406.652V406.652C1234.73 407.53 1233.55 408.406 1232.86 407.657V407.657C1232.47 407.233 1231.78 407.312 1231.5 407.812V407.812C1231 408.697 1229.65 408.11 1229.95 407.139V407.139C1230.12 406.589 1229.71 406.032 1229.13 406.036V406.036C1228.12 406.043 1227.95 404.58 1228.94 404.358V404.358C1229.5 404.233 1229.78 403.596 1229.49 403.099V403.099C1228.97 402.222 1230.16 401.346 1230.85 402.095V402.095C1231.24 402.519 1231.93 402.44 1232.21 401.94V401.94Z"
          fill="#FCE8DE"
        />
        <path
          d="M1345.07 203.768C1345.57 202.883 1346.92 203.47 1346.62 204.441V204.441C1346.45 204.991 1346.86 205.549 1347.43 205.544V205.544C1348.45 205.537 1348.62 207 1347.63 207.222V207.222C1347.06 207.348 1346.79 207.984 1347.08 208.481V208.481C1347.59 209.358 1346.41 210.234 1345.72 209.485V209.485C1345.33 209.061 1344.64 209.14 1344.36 209.64V209.64C1343.86 210.525 1342.5 209.938 1342.81 208.967V208.967C1342.98 208.418 1342.57 207.86 1341.99 207.864V207.864C1340.98 207.871 1340.81 206.408 1341.8 206.186V206.186C1342.36 206.061 1342.64 205.424 1342.35 204.928V204.928C1341.83 204.05 1343.02 203.174 1343.71 203.923V203.923C1344.1 204.347 1344.79 204.269 1345.07 203.768V203.768Z"
          fill="#FCE8DE"
        />
        <path
          d="M706.025 490.448C706.617 489.406 708.208 490.097 707.849 491.241L705.783 497.827C705.58 498.474 706.067 499.131 706.745 499.126L713.646 499.076C714.845 499.067 715.041 500.791 713.871 501.052L707.136 502.556C706.474 502.703 706.148 503.453 706.491 504.038L709.985 509.99C710.592 511.024 709.197 512.055 708.386 511.173L703.716 506.091C703.257 505.592 702.445 505.685 702.11 506.274L698.703 512.276C698.111 513.318 696.52 512.627 696.879 511.483L698.944 504.898C699.147 504.251 698.661 503.594 697.983 503.598L691.081 503.648C689.883 503.657 689.686 501.933 690.856 501.672L697.592 500.168C698.254 500.021 698.58 499.271 698.237 498.686L694.743 492.734C694.136 491.701 695.53 490.669 696.341 491.551L701.012 496.633C701.471 497.132 702.283 497.04 702.618 496.45L706.025 490.448Z"
          fill="#FCE8DE"
        />
        <path
          opacity="0.4"
          d="M390.408 19.9795C391 18.9371 392.59 19.6287 392.232 20.7725L390.166 27.3578C389.963 28.0048 390.449 28.6619 391.128 28.657L398.029 28.6072C399.228 28.5986 399.424 30.322 398.254 30.5832L391.518 32.087C390.857 32.2347 390.531 32.9844 390.874 33.5692L394.368 39.5211C394.975 40.5548 393.58 41.5866 392.769 40.704L388.099 35.6226C387.64 35.1233 386.828 35.2158 386.493 35.8055L383.085 41.8072C382.493 42.8496 380.903 42.158 381.262 41.0142L383.327 34.4289C383.53 33.7819 383.044 33.1248 382.366 33.1297L375.464 33.1795C374.266 33.1881 374.069 31.4647 375.239 31.2035L381.975 29.6997C382.637 29.552 382.963 28.8023 382.619 28.2175L379.126 22.2656C378.519 21.2318 379.913 20.2001 380.724 21.0827L385.395 26.1641C385.853 26.6634 386.666 26.5709 387 25.9812L390.408 19.9795Z"
          fill="#FCE8DE"
        />
        <path
          opacity="0.5"
          d="M900.627 44.8662C901.219 43.8238 902.809 44.5154 902.45 45.6592L900.385 52.2445C900.182 52.8915 900.668 53.5486 901.346 53.5437L908.248 53.4939C909.446 53.4853 909.643 55.2087 908.473 55.4699L901.737 56.9737C901.075 57.1214 900.749 57.8711 901.093 58.4559L904.586 64.4078C905.193 65.4416 903.799 66.4733 902.988 65.5907L898.318 60.5093C897.859 60.01 897.046 60.1025 896.712 60.6922L893.304 66.6939C892.712 67.7364 891.122 67.0447 891.48 65.9009L893.546 59.3157C893.749 58.6686 893.263 58.0115 892.584 58.0164L885.683 58.0662C884.484 58.0749 884.288 56.3515 885.458 56.0903L892.194 54.5864C892.856 54.4387 893.181 53.689 892.838 53.1042L889.344 47.1523C888.738 46.1186 890.132 45.0868 890.943 45.9694L895.613 51.0509C896.072 51.5501 896.884 51.4576 897.219 50.8679L900.627 44.8662Z"
          fill="#FCE8DE"
        />
        <path
          opacity="0.5"
          d="M376.956 377.979C377.548 376.937 379.139 377.629 378.78 378.772L378.653 379.176C378.45 379.823 378.937 380.48 379.615 380.475L380.038 380.472C381.237 380.464 381.433 382.187 380.263 382.448L379.85 382.54C379.188 382.688 378.862 383.438 379.206 384.023L379.42 384.388C380.027 385.421 378.632 386.453 377.821 385.57L377.535 385.259C377.076 384.76 376.264 384.852 375.929 385.442L375.72 385.81C375.128 386.852 373.537 386.161 373.896 385.017L374.023 384.613C374.226 383.966 373.74 383.309 373.061 383.314L372.638 383.317C371.44 383.326 371.243 381.602 372.413 381.341L372.826 381.249C373.488 381.101 373.814 380.351 373.471 379.767L373.256 379.402C372.65 378.368 374.044 377.336 374.855 378.219L375.141 378.53C375.6 379.029 376.413 378.937 376.747 378.347L376.956 377.979Z"
          fill="#FCE8DE"
        />
        <path
          opacity="0.3"
          d="M1073.35 414.429C1073.3 413.231 1075.02 412.979 1075.32 414.14L1080 432.327C1080.17 432.984 1080.93 433.285 1081.5 432.923L1097.38 422.898C1098.4 422.258 1099.47 423.618 1098.62 424.458L1085.21 437.606C1084.72 438.081 1084.84 438.89 1085.44 439.205L1102.07 447.945C1103.13 448.503 1102.49 450.115 1101.33 449.794L1083.24 444.755C1082.59 444.573 1081.95 445.08 1081.97 445.758L1082.72 464.523C1082.76 465.721 1081.05 465.973 1080.75 464.812L1076.07 446.625C1075.9 445.968 1075.14 445.666 1074.56 446.028L1058.68 456.054C1057.67 456.694 1056.59 455.334 1057.45 454.494L1070.86 441.346C1071.34 440.871 1071.22 440.062 1070.62 439.747L1054 431.007C1052.94 430.449 1053.58 428.837 1054.74 429.158L1072.83 434.197C1073.48 434.379 1074.12 433.872 1074.09 433.194L1073.35 414.429Z"
          fill="#FCE8DE"
        />
        <path
          opacity="0.5"
          d="M1357.68 387.044C1358.27 386.002 1359.87 386.693 1359.51 387.837L1357.56 394.03C1357.36 394.677 1357.85 395.334 1358.53 395.329L1365.02 395.283C1366.21 395.274 1366.41 396.997 1365.24 397.259L1358.91 398.673C1358.24 398.821 1357.92 399.57 1358.26 400.155L1361.55 405.752C1362.15 406.786 1360.76 407.818 1359.95 406.935L1355.56 402.157C1355.1 401.657 1354.29 401.75 1353.95 402.339L1350.75 407.984C1350.15 409.026 1348.56 408.334 1348.92 407.191L1350.86 400.998C1351.07 400.351 1350.58 399.694 1349.9 399.698L1343.41 399.745C1342.21 399.754 1342.02 398.03 1343.19 397.769L1349.52 396.355C1350.18 396.207 1350.51 395.458 1350.17 394.873L1346.88 389.276C1346.27 388.242 1347.67 387.21 1348.48 388.093L1352.87 392.871C1353.33 393.371 1354.14 393.278 1354.48 392.688L1357.68 387.044Z"
          fill="#FCE8DE"
        />
        <path
          d="M1351.63 56.9472C1352.45 56.135 1353.76 57.1238 1353.21 58.1359L1352.49 59.4627C1352.28 59.8509 1352.34 60.3322 1352.66 60.6461L1353.72 61.7188C1354.53 62.5371 1353.54 63.8533 1352.53 63.3011L1351.21 62.5771C1350.82 62.3653 1350.34 62.4337 1350.02 62.7452L1348.95 63.8099C1348.13 64.6221 1346.81 63.6333 1347.37 62.6212L1348.09 61.2945C1348.3 60.9062 1348.23 60.4249 1347.92 60.111L1346.86 59.0383C1346.05 58.22 1347.03 56.9038 1348.05 57.4561L1349.37 58.18C1349.76 58.3918 1350.24 58.3235 1350.56 58.0119L1351.63 56.9472Z"
          fill="#FCE8DE"
        />
        <path
          d="M781.833 59.0019C782.651 58.1897 783.967 59.1785 783.415 60.1906L782.691 61.5173C782.479 61.9056 782.547 62.3869 782.859 62.7008L783.924 63.7735C784.736 64.5918 783.747 65.908 782.735 65.3558L781.408 64.6318C781.02 64.42 780.539 64.4883 780.225 64.7999L779.152 65.8646C778.334 66.6768 777.018 65.688 777.57 64.6759L778.294 63.3492C778.506 62.9609 778.437 62.4796 778.126 62.1657L777.061 61.093C776.249 60.2747 777.238 58.9585 778.25 59.5107L779.576 60.2347C779.965 60.4465 780.446 60.3782 780.76 60.0666L781.833 59.0019Z"
          fill="#FCE8DE"
        />
        <path
          d="M696.792 117.936C696.366 116.865 697.791 116.042 698.506 116.946L704.168 124.117C704.442 124.464 704.912 124.59 705.323 124.426L713.811 121.048C714.883 120.621 715.706 122.047 714.801 122.761L707.631 128.424C707.284 128.698 707.158 129.167 707.321 129.578L710.7 138.067C711.126 139.138 709.7 139.961 708.986 139.056L703.324 131.886C703.05 131.539 702.58 131.413 702.169 131.577L693.68 134.955C692.609 135.382 691.786 133.956 692.691 133.241L699.861 127.579C700.208 127.305 700.334 126.836 700.17 126.425L696.792 117.936Z"
          fill="#FCE8DE"
        />
        <path
          opacity="0.2"
          d="M748.939 317.406C748.512 316.335 749.938 315.512 750.653 316.416L761.348 329.96C761.622 330.307 762.092 330.433 762.503 330.27L778.537 323.888C779.608 323.462 780.431 324.887 779.527 325.602L765.983 336.297C765.636 336.571 765.51 337.041 765.673 337.452L772.055 353.486C772.481 354.558 771.056 355.381 770.341 354.476L759.646 340.932C759.372 340.585 758.902 340.459 758.491 340.623L742.457 347.004C741.385 347.431 740.562 346.005 741.467 345.29L755.011 334.595C755.358 334.321 755.484 333.851 755.32 333.44L748.939 317.406Z"
          fill="#FCE8DE"
        />
        <path
          d="M932.155 141.617C932.163 140.464 933.794 140.237 934.115 141.345L937.023 151.352C937.146 151.777 937.534 152.07 937.976 152.073L948.397 152.144C949.55 152.152 949.777 153.783 948.669 154.105L938.662 157.012C938.237 157.136 937.944 157.523 937.941 157.966L937.87 168.386C937.862 169.539 936.231 169.766 935.909 168.659L933.002 158.651C932.878 158.227 932.491 157.934 932.048 157.93L921.628 157.859C920.475 157.851 920.248 156.22 921.355 155.899L931.363 152.991C931.787 152.868 932.081 152.48 932.084 152.038L932.155 141.617Z"
          fill="#FCE8DE"
        />
        <path
          d="M719.891 754.419C720.449 753.41 721.99 753.991 721.743 755.117L720.47 760.926C720.376 761.358 720.576 761.801 720.963 762.015L726.166 764.894C727.175 765.452 726.594 766.992 725.468 766.745L719.659 765.473C719.227 765.378 718.784 765.578 718.57 765.965L715.692 771.169C715.133 772.178 713.593 771.597 713.84 770.471L715.112 764.662C715.207 764.23 715.007 763.787 714.62 763.573L709.416 760.694C708.408 760.136 708.988 758.595 710.115 758.842L715.923 760.115C716.355 760.21 716.798 760.009 717.012 759.622L719.891 754.419Z"
          fill="#FCE8DE"
        />
        <path
          d="M1215.01 901.028C1215.61 899.986 1217.2 900.677 1216.84 901.821L1211.22 919.74C1211.01 920.387 1211.5 921.045 1212.18 921.04L1230.96 920.904C1232.16 920.895 1232.35 922.619 1231.18 922.88L1212.85 926.972C1212.19 927.12 1211.87 927.87 1212.21 928.454L1221.72 944.65C1222.32 945.684 1220.93 946.716 1220.12 945.833L1207.41 932.006C1206.95 931.507 1206.14 931.599 1205.8 932.189L1196.53 948.52C1195.94 949.563 1194.35 948.871 1194.71 947.727L1200.33 929.808C1200.53 929.161 1200.05 928.504 1199.37 928.509L1180.59 928.644C1179.39 928.653 1179.19 926.929 1180.36 926.668L1198.69 922.576C1199.35 922.428 1199.68 921.679 1199.34 921.094L1189.83 904.898C1189.22 903.864 1190.62 902.833 1191.43 903.715L1204.14 917.542C1204.59 918.042 1205.41 917.949 1205.74 917.359L1215.01 901.028Z"
          fill="#FCE8DE"
        />
        <path
          d="M1374.51 550.213C1375.01 549.328 1376.36 549.915 1376.06 550.886V550.886C1375.88 551.436 1376.3 551.994 1376.87 551.99V551.99C1377.89 551.982 1378.06 553.446 1377.06 553.667V553.667C1376.5 553.793 1376.22 554.429 1376.52 554.926V554.926C1377.03 555.804 1375.85 556.68 1375.16 555.93V555.93C1374.77 555.506 1374.08 555.585 1373.8 556.086V556.086C1373.29 556.971 1371.94 556.383 1372.25 555.412V555.412C1372.42 554.863 1372.01 554.305 1371.43 554.309V554.309C1370.41 554.316 1370.25 552.853 1371.24 552.631V552.631C1371.8 552.506 1372.08 551.869 1371.79 551.373V551.373C1371.27 550.495 1372.46 549.619 1373.14 550.369V550.369C1373.53 550.792 1374.22 550.714 1374.51 550.213V550.213Z"
          fill="#FCE8DE"
        />
        <path
          d="M641.833 439.002C642.651 438.19 643.967 439.179 643.415 440.191L642.691 441.517C642.479 441.906 642.547 442.387 642.859 442.701L643.924 443.773C644.736 444.592 643.747 445.908 642.735 445.356L641.408 444.632C641.02 444.42 640.539 444.488 640.225 444.8L639.152 445.865C638.334 446.677 637.018 445.688 637.57 444.676L638.294 443.349C638.506 442.961 638.437 442.48 638.126 442.166L637.061 441.093C636.249 440.275 637.238 438.958 638.25 439.511L639.576 440.235C639.965 440.447 640.446 440.378 640.76 440.067L641.833 439.002Z"
          fill="#FCE8DE"
        />
        <path
          d="M706.706 855.862C706.28 854.79 707.705 853.967 708.42 854.872L714.082 862.042C714.356 862.39 714.826 862.515 715.237 862.352L723.725 858.973C724.797 858.547 725.62 859.973 724.715 860.687L717.545 866.349C717.198 866.624 717.072 867.093 717.235 867.504L720.614 875.993C721.04 877.064 719.615 877.887 718.9 876.982L713.238 869.812C712.964 869.465 712.494 869.339 712.083 869.503L703.595 872.881C702.523 873.307 701.7 871.882 702.605 871.167L709.775 865.505C710.122 865.231 710.248 864.761 710.085 864.35L706.706 855.862Z"
          fill="#FCE8DE"
        />
        <path
          d="M792.155 521.617C792.163 520.464 793.794 520.237 794.115 521.345L797.023 531.352C797.146 531.777 797.534 532.07 797.976 532.073L808.397 532.144C809.55 532.152 809.777 533.783 808.669 534.105L798.662 537.012C798.237 537.136 797.944 537.523 797.941 537.966L797.87 548.386C797.862 549.539 796.231 549.766 795.909 548.659L793.002 538.651C792.878 538.227 792.491 537.934 792.048 537.93L781.628 537.859C780.475 537.851 780.248 536.22 781.355 535.899L791.363 532.991C791.787 532.868 792.081 532.48 792.084 532.038L792.155 521.617Z"
          fill="#FCE8DE"
        />
        <path
          d="M980.767 934.156C981.74 933.538 982.813 934.787 982.056 935.657L976.754 941.751C976.463 942.085 976.427 942.57 976.664 942.943L980.99 949.766C981.607 950.739 980.359 951.812 979.489 951.056L973.394 945.753C973.061 945.463 972.576 945.426 972.202 945.663L965.38 949.989C964.406 950.606 963.333 949.358 964.09 948.488L969.393 942.394C969.683 942.06 969.72 941.575 969.483 941.202L965.157 934.379C964.539 933.405 965.788 932.332 966.658 933.089L972.752 938.392C973.086 938.682 973.571 938.719 973.944 938.482L980.767 934.156Z"
          fill="#FCE8DE"
        />
        <path
          d="M1344.18 625.457C1344.09 626.607 1342.45 626.726 1342.2 625.6L1340.79 619.187C1340.69 618.755 1340.32 618.437 1339.88 618.405L1333.33 617.93C1332.18 617.846 1332.06 616.204 1333.19 615.956L1339.6 614.54C1340.03 614.445 1340.35 614.077 1340.38 613.636L1340.86 607.086C1340.94 605.936 1342.58 605.817 1342.83 606.943L1344.25 613.356C1344.34 613.788 1344.71 614.106 1345.15 614.138L1351.7 614.613C1352.85 614.696 1352.97 616.338 1351.85 616.587L1345.43 618.002C1345 618.097 1344.68 618.465 1344.65 618.906L1344.18 625.457Z"
          fill="#FCE8DE"
        />
        <path
          d="M1298.88 809.766C1298.45 810.833 1296.85 810.437 1296.96 809.29L1297.49 803.936C1297.53 803.496 1297.28 803.08 1296.87 802.912L1291.89 800.879C1290.82 800.443 1291.22 798.845 1292.36 798.958L1297.72 799.484C1298.16 799.527 1298.58 799.276 1298.74 798.867L1300.78 793.886C1301.21 792.819 1302.81 793.214 1302.7 794.362L1302.17 799.716C1302.13 800.156 1302.38 800.572 1302.79 800.74L1307.77 802.773C1308.84 803.209 1308.44 804.807 1307.29 804.694L1301.94 804.168C1301.5 804.125 1301.08 804.376 1300.92 804.785L1298.88 809.766Z"
          fill="#FCE8DE"
        />
        <path
          d="M141.811 739.473C141.376 740.54 139.778 740.144 139.89 738.997L140.417 733.643C140.46 733.203 140.209 732.787 139.799 732.619L134.819 730.586C133.751 730.15 134.147 728.552 135.294 728.665L140.648 729.191C141.088 729.234 141.505 728.983 141.672 728.574L143.705 723.593C144.141 722.526 145.739 722.921 145.626 724.069L145.1 729.423C145.057 729.863 145.308 730.279 145.717 730.447L150.698 732.48C151.766 732.916 151.37 734.514 150.222 734.401L144.868 733.875C144.428 733.832 144.012 734.083 143.845 734.492L141.811 739.473Z"
          fill="#FCE8DE"
        />
        <path
          d="M190.533 958.519C189.941 959.561 188.351 958.87 188.709 957.726L194.33 939.806C194.533 939.159 194.047 938.502 193.369 938.507L174.589 938.643C173.39 938.651 173.194 936.928 174.364 936.667L192.693 932.575C193.355 932.427 193.681 931.677 193.337 931.092L183.83 914.897C183.223 913.863 184.618 912.831 185.429 913.714L198.137 927.541C198.596 928.04 199.408 927.948 199.743 927.358L209.015 911.027C209.607 909.984 211.198 910.676 210.839 911.82L205.219 929.739C205.016 930.386 205.502 931.043 206.18 931.038L224.96 930.903C226.158 930.894 226.355 932.617 225.185 932.879L206.856 936.971C206.194 937.118 205.868 937.868 206.211 938.453L215.719 954.649C216.325 955.683 214.931 956.714 214.12 955.832L201.412 942.004C200.953 941.505 200.14 941.598 199.806 942.187L190.533 958.519Z"
          fill="#FCE8DE"
        />
        <path
          opacity="0.4"
          d="M1356.14 882.831C1355.55 883.873 1353.96 883.182 1354.31 882.038L1355.46 878.392C1355.66 877.745 1355.18 877.088 1354.5 877.093L1350.68 877.12C1349.48 877.129 1349.28 875.405 1350.45 875.144L1354.18 874.312C1354.84 874.164 1355.17 873.414 1354.82 872.829L1352.89 869.534C1352.28 868.5 1353.68 867.469 1354.49 868.351L1357.07 871.165C1357.53 871.664 1358.35 871.571 1358.68 870.982L1360.57 867.659C1361.16 866.616 1362.75 867.308 1362.39 868.452L1361.25 872.098C1361.04 872.745 1361.53 873.402 1362.21 873.397L1366.03 873.369C1367.23 873.361 1367.42 875.084 1366.25 875.345L1362.53 876.178C1361.86 876.326 1361.54 877.075 1361.88 877.66L1363.82 880.955C1364.42 881.989 1363.03 883.021 1362.22 882.138L1359.63 879.325C1359.17 878.826 1358.36 878.918 1358.03 879.508L1356.14 882.831Z"
          fill="#FCE8DE"
        />
        <path
          d="M1168.79 72.0837C1168.29 72.9688 1166.94 72.3815 1167.24 71.4104V71.4104C1167.41 70.861 1167 70.303 1166.42 70.3072V70.3072C1165.41 70.3145 1165.24 68.8513 1166.23 68.6295V68.6295C1166.8 68.504 1167.07 67.8675 1166.78 67.371V67.371C1166.27 66.4932 1167.45 65.6172 1168.14 66.3666V66.3666C1168.53 66.7905 1169.22 66.7119 1169.5 66.2112V66.2112C1170 65.3261 1171.35 65.9134 1171.05 66.8846V66.8846C1170.88 67.4339 1171.29 67.9919 1171.87 67.9877V67.9877C1172.88 67.9804 1173.05 69.4437 1172.06 69.6655V69.6655C1171.5 69.7909 1171.22 70.4274 1171.51 70.924V70.924C1172.03 71.8017 1170.84 72.6778 1170.15 71.9284V71.9284C1169.76 71.5045 1169.07 71.583 1168.79 72.0837V72.0837Z"
          fill="#FCE8DE"
        />
        <path
          d="M22.0549 714.002C21.5523 714.887 20.2017 714.3 20.5063 713.328V713.328C20.6786 712.779 20.2658 712.221 19.69 712.225V712.225C18.6723 712.233 18.5056 710.769 19.4989 710.547V710.547C20.0608 710.422 20.3376 709.785 20.0461 709.289V709.289C19.5309 708.411 20.7148 707.535 21.4035 708.285V708.285C21.7931 708.708 22.4828 708.63 22.767 708.129V708.129C23.2696 707.244 24.6202 707.831 24.3156 708.803V708.803C24.1432 709.352 24.5561 709.91 25.1318 709.906V709.906C26.1496 709.898 26.3163 711.362 25.323 711.583V711.583C24.7611 711.709 24.4843 712.345 24.7758 712.842V712.842C25.291 713.72 24.1071 714.596 23.4184 713.846V713.846C23.0288 713.422 22.3391 713.501 22.0549 714.002V714.002Z"
          fill="#FCE8DE"
        />
        <path
          d="M378.272 662.146C377.68 663.188 376.089 662.496 376.448 661.352L378.514 654.767C378.716 654.12 378.23 653.463 377.552 653.468L370.651 653.518C369.452 653.526 369.256 651.803 370.426 651.542L377.161 650.038C377.823 649.89 378.149 649.141 377.806 648.556L374.312 642.604C373.705 641.57 375.1 640.538 375.911 641.421L380.581 646.502C381.04 647.002 381.852 646.909 382.187 646.319L385.594 640.318C386.186 639.275 387.777 639.967 387.418 641.111L385.353 647.696C385.15 648.343 385.636 649 386.314 648.995L393.215 648.946C394.414 648.937 394.61 650.66 393.44 650.921L386.705 652.425C386.043 652.573 385.717 653.323 386.06 653.907L389.554 659.859C390.161 660.893 388.767 661.925 387.955 661.042L383.285 655.961C382.826 655.462 382.014 655.554 381.679 656.144L378.272 662.146Z"
          fill="#FCE8DE"
        />
        <path
          opacity="0.4"
          d="M976.717 897.79C976.125 898.832 974.535 898.141 974.893 896.997L976.959 890.412C977.162 889.765 976.676 889.108 975.997 889.113L969.096 889.162C967.897 889.171 967.701 887.448 968.871 887.186L975.607 885.683C976.268 885.535 976.594 884.785 976.251 884.2L972.757 878.248C972.15 877.215 973.545 876.183 974.356 877.066L979.026 882.147C979.485 882.646 980.297 882.554 980.632 881.964L984.04 875.962C984.632 874.92 986.222 875.612 985.863 876.755L983.798 883.341C983.595 883.988 984.081 884.645 984.759 884.64L991.661 884.59C992.859 884.581 993.056 886.305 991.886 886.566L985.15 888.07C984.488 888.218 984.162 888.967 984.506 889.552L987.999 895.504C988.606 896.538 987.212 897.569 986.401 896.687L981.73 891.605C981.272 891.106 980.459 891.199 980.125 891.788L976.717 897.79Z"
          fill="#FCE8DE"
        />
        <path
          opacity="0.5"
          d="M252.701 813.274C252.11 814.317 250.519 813.625 250.878 812.481L252.943 805.896C253.146 805.249 252.66 804.592 251.982 804.597L245.08 804.647C243.882 804.655 243.685 802.932 244.855 802.671L251.591 801.167C252.253 801.019 252.579 800.27 252.236 799.685L248.742 793.733C248.135 792.699 249.529 791.667 250.34 792.55L255.011 797.631C255.469 798.131 256.282 798.038 256.616 797.448L260.024 791.447C260.616 790.404 262.207 791.096 261.848 792.24L259.782 798.825C259.579 799.472 260.066 800.129 260.744 800.124L267.645 800.074C268.844 800.066 269.04 801.789 267.87 802.05L261.134 803.554C260.473 803.702 260.147 804.452 260.49 805.036L263.984 810.988C264.591 812.022 263.196 813.054 262.385 812.171L257.715 807.09C257.256 806.59 256.444 806.683 256.109 807.273L252.701 813.274Z"
          fill="#FCE8DE"
        />
        <path
          opacity="0.5"
          d="M9.44242 530.725C8.85056 531.768 7.25988 531.076 7.61864 529.932L9.56115 523.739C9.7641 523.092 9.27786 522.435 8.59977 522.44L2.10947 522.487C0.910769 522.496 0.714428 520.772 1.88436 520.511L8.21888 519.097C8.88069 518.949 9.20666 518.199 8.86338 517.615L5.57766 512.017C4.97082 510.983 6.36516 509.952 7.17633 510.834L11.5683 515.613C12.0272 516.112 12.8394 516.02 13.1742 515.43L16.3788 509.786C16.9707 508.743 18.5614 509.435 18.2026 510.579L16.2601 516.772C16.0571 517.419 16.5434 518.076 17.2215 518.071L23.7118 518.024C24.9105 518.016 25.1068 519.739 23.9369 520L17.6024 521.414C16.9405 521.562 16.6146 522.312 16.9579 522.897L20.2436 528.494C20.8504 529.528 19.4561 530.56 18.6449 529.677L14.2529 524.898C13.794 524.399 12.9818 524.491 12.647 525.081L9.44242 530.725Z"
          fill="#FCE8DE"
        />
        <path
          d="M414.954 944.795C414.135 945.607 412.819 944.618 413.371 943.606L415.587 939.546C415.799 939.158 415.73 938.676 415.419 938.362L412.16 935.079C411.348 934.261 412.337 932.945 413.349 933.497L417.41 935.713C417.798 935.925 418.279 935.856 418.593 935.545L421.876 932.286C422.694 931.474 424.011 932.463 423.458 933.475L421.243 937.535C421.031 937.924 421.099 938.405 421.411 938.719L424.669 942.002C425.482 942.82 424.493 944.136 423.481 943.584L419.42 941.368C419.032 941.157 418.551 941.225 418.237 941.537L414.954 944.795Z"
          fill="#FCE8DE"
        />
        <path
          d="M15.4956 860.822C14.6772 861.635 13.361 860.646 13.9133 859.634L14.6372 858.307C14.8491 857.919 14.7807 857.437 14.4691 857.123L13.4045 856.051C12.5922 855.232 13.5811 853.916 14.5932 854.468L15.9199 855.192C16.3081 855.404 16.7894 855.336 17.1033 855.024L18.176 853.96C18.9944 853.147 20.3106 854.136 19.7583 855.148L19.0344 856.475C18.8225 856.863 18.8909 857.345 19.2025 857.659L20.2672 858.731C21.0794 859.55 20.0905 860.866 19.0784 860.313L17.7517 859.59C17.3635 859.378 16.8822 859.446 16.5683 859.758L15.4956 860.822Z"
          fill="#FCE8DE"
        />
        <path
          d="M585.285 858.768C584.466 859.58 583.15 858.591 583.702 857.579L584.426 856.252C584.638 855.864 584.57 855.383 584.258 855.069L583.194 853.996C582.381 853.178 583.37 851.862 584.382 852.414L585.709 853.138C586.097 853.35 586.579 853.281 586.892 852.97L587.965 851.905C588.783 851.093 590.1 852.082 589.547 853.094L588.823 854.42C588.612 854.809 588.68 855.29 588.992 855.604L590.056 856.677C590.868 857.495 589.88 858.811 588.867 858.259L587.541 857.535C587.153 857.323 586.671 857.391 586.357 857.703L585.285 858.768Z"
          fill="#FCE8DE"
        />
        <path
          opacity="0.2"
          d="M768.1 958.289C768.527 959.361 767.101 960.184 766.386 959.279L755.691 945.735C755.417 945.388 754.947 945.262 754.536 945.426L738.502 951.807C737.431 952.234 736.608 950.808 737.512 950.093L751.056 939.398C751.403 939.124 751.529 938.654 751.366 938.243L744.984 922.209C744.558 921.138 745.983 920.314 746.698 921.219L757.393 934.763C757.668 935.11 758.137 935.236 758.548 935.073L774.582 928.691C775.654 928.265 776.477 929.69 775.572 930.405L762.028 941.1C761.681 941.374 761.555 941.844 761.719 942.255L768.1 958.289Z"
          fill="#FCE8DE"
        />
        <path
          d="M434.97 776.153C434.962 777.306 433.331 777.532 433.01 776.425L430.102 766.418C429.979 765.993 429.591 765.7 429.149 765.697L418.728 765.625C417.575 765.617 417.348 763.987 418.456 763.665L428.463 760.757C428.888 760.634 429.181 760.246 429.184 759.804L429.255 749.383C429.263 748.23 430.894 748.004 431.216 749.111L434.123 759.118C434.247 759.543 434.634 759.836 435.077 759.839L445.497 759.911C446.65 759.919 446.877 761.549 445.77 761.871L435.762 764.779C435.338 764.902 435.044 765.29 435.041 765.732L434.97 776.153Z"
          fill="#FCE8DE"
        />
      </pattern>
    </defs>
    <rect width="100%" height="100%" fill="url(#specialGuestBg)" />
  </svg>
);
