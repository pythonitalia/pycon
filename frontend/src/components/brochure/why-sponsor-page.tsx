import { SnakeDNA } from "@python-italia/pycon-styleguide/illustrations";
import { compile } from "~/helpers/markdown";

const Snake1 = (props: React.SVGProps<SVGSVGElement>) => (
  <svg
    width={147}
    height={146}
    viewBox="0 0 147 146"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    {...props}
  >
    <mask
      id="a"
      style={{
        maskType: "alpha",
      }}
      maskUnits="userSpaceOnUse"
      x={0}
      y={0}
      width={146}
      height={146}
    >
      <path d="M145.999.063H.809v145.19h145.19V.063Z" fill="#79CADF" />
    </mask>
    <g mask="url(#a)">
      <path d="M145.999.063H.809v145.19h145.19V.063Z" fill="#79CADF" />
      <path
        d="M148.258 96.001H-1.445V71.257h.598c7.475-7.186 22.393-7.186 29.848 0 7.474 7.186 22.383 7.186 29.858 0 7.454-7.186 22.372-7.186 29.847 0 7.455 7.186 22.373 7.186 29.848 0 7.413-7.135 22.177-7.186 29.704-.124v24.868Z"
        fill="#FDE8DE"
      />
      <path
        d="M118.554 71.252c-7.475 7.186-22.393 7.186-29.848 0-7.475-7.186-22.383-7.186-29.847 0-7.475 7.186-22.394 7.186-29.859 0-7.454-7.186-22.372-7.186-29.847 0h-.598V46.508h149.692v24.61c-7.526-7.062-22.29-7.01-29.703.124"
        fill="#EF7A5C"
      />
      <path
        d="M148.258 71.134v24.868H-1.445V46.523h149.703v24.61Z"
        stroke="#1C1D1C"
        strokeWidth={3.62}
        strokeMiterlimit={10}
      />
      <path
        d="M148.402 71.257s-.093-.093-.145-.124c-7.526-7.062-22.29-7.01-29.703.124-7.475 7.186-22.383 7.186-29.848 0-7.475-7.186-22.383-7.186-29.848 0-7.475 7.186-22.383 7.186-29.858 0-7.454-7.186-22.373-7.186-29.848 0"
        stroke="#1C1D1C"
        strokeWidth={3.62}
        strokeMiterlimit={1}
      />
    </g>
  </svg>
);

const Snake2 = (props: React.SVGProps<SVGSVGElement>) => (
  <svg
    width={150}
    height={150}
    viewBox="0 0 150 150"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    {...props}
  >
    <mask
      id="a"
      style={{
        maskType: "alpha",
      }}
      maskUnits="userSpaceOnUse"
      x={0}
      y={0}
      width={150}
      height={150}
    >
      <path d="M150 0H0v150h150V0Z" fill="#79CADF" />
    </mask>
    <g mask="url(#a)">
      <path
        d="M149.88 27.862V-.008H25.56c-4.83 7.38-7.63 16.22-7.63 25.7 0 25.96 21.04 47.02 47.01 47.02h6.5c-12.29 0-22.11-10.33-22.11-22.61s9.97-22.24 22.24-22.24h78.32-.01Z"
        fill="#EF7A5C"
      />
      <path
        d="M149.88 149.889V27.859H71.56c-12.27 0-22.24 9.95-22.24 22.24s9.83 22.61 22.11 22.61h20.42c27.47 0 49.79 21.89 49.79 49.34 0 10.32-3.14 19.89-8.51 27.83h16.74l.01.01Z"
        fill="#6778B9"
      />
      <path
        d="M133.14 149.89a49.545 49.545 0 0 0 8.51-27.83c0-27.45-22.33-49.34-49.79-49.34H64.94c-25.97 0-47.01-21.07-47.01-47.02 0-9.48 2.81-18.31 7.63-25.7h-1.39C14.24 11.3 8.23 26.11 8.23 42.33c0 35.45 28.74 64.2 64.21 64.2h25.5c17.79.1 32.19 14.56 32.19 32.36 0 3.87-.67 7.57-1.92 11h4.93ZM133.141 149.891h-4.93a32.353 32.353 0 0 1-11.75 15.42 50.155 50.155 0 0 0 16.68-15.42Z"
        fill="#FDE8DE"
      />
      <path
        d="M128.221 149.891a32.08 32.08 0 0 0 1.92-11c0-17.8-14.41-32.26-32.19-32.36H80.96v.16c12.61 0 22.83 10.23 22.83 22.85 0 8.87-5.05 16.57-12.46 20.34h36.9l-.01.01Z"
        fill="#EF7A5C"
      />
      <path
        d="M91.32 149.888c7.41-3.78 12.46-11.47 12.46-20.34 0-12.62-10.22-22.85-22.83-22.85v-.16h-8.51c-35.47 0-64.21-28.75-64.21-64.2 0-16.23 6.01-31.03 15.94-42.33H-.02v149.89h91.33l.01-.01Z"
        fill="#6778B9"
      />
      <path
        d="M24.178-.003c-9.93 11.3-15.94 26.1-15.94 42.33 0 35.45 28.74 64.2 64.21 64.2h25.5c17.78.1 32.19 14.56 32.19 32.36 0 3.86-.67 7.57-1.92 11a32.353 32.353 0 0 1-11.75 15.42m-18.69 5.95c.54 0 1.08 0 1.62-.04h.04m0 0c6.32-.31 12.17-2.47 17.03-5.91m-17.03 5.91c6.11-.92 11.86-2.96 17.03-5.91m0 0a50.155 50.155 0 0 0 16.68-15.42 49.545 49.545 0 0 0 8.51-27.83c0-27.45-22.33-49.34-49.79-49.34h-20.42c-12.29 0-22.12-10.33-22.12-22.61s9.97-22.24 22.24-22.24h78.32m-68.93 78.82c12.61 0 22.83 10.23 22.83 22.85 0 8.87-5.05 16.57-12.46 20.34-3.12 1.6-6.64 2.5-10.37 2.5M30.318-6.133a47.774 47.774 0 0 0-4.76 6.12c-4.83 7.38-7.63 16.21-7.63 25.7 0 25.96 21.04 47.02 47.01 47.02h6.5"
        stroke="#1C1D1C"
        strokeWidth={3.74}
        strokeMiterlimit={10}
      />
    </g>
  </svg>
);

const Snake3 = (props: React.SVGProps<SVGSVGElement>) => (
  <svg
    width={149}
    height={149}
    viewBox="0 0 149 149"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    {...props}
  >
    <mask
      id="a"
      style={{
        maskType: "alpha",
      }}
      maskUnits="userSpaceOnUse"
      x={0}
      y={0}
      width={149}
      height={149}
    >
      <path d="M148.82 0H0v148.82h148.82V0Z" fill="#F7B03C" />
    </mask>
    <g mask="url(#a)">
      <path d="M148.82 0H0v148.82h148.82V0Z" fill="#F7B03C" />
      <path
        d="M-94.098 49.14h144.48v23.92h-.58c-7.21 6.95-21.61 6.95-28.8 0-7.21-6.95-21.61-6.95-28.82 0-7.2 6.95-21.59 6.95-28.8 0-7.2-6.95-21.59-6.95-28.8 0-7.15 6.9-21.4 6.95-28.66.12V49.14h-.02Z"
        fill="#FDE8DE"
      />
      <path
        d="M-65.437 73.064c7.21-6.95 21.61-6.95 28.8 0 7.21 6.95 21.61 6.95 28.8 0 7.21-6.95 21.61-6.95 28.82 0 7.2 6.95 21.59 6.95 28.8 0h.58v23.92h-144.48v-23.79c7.26 6.82 21.51 6.78 28.66-.12"
        fill="#EF7A5C"
      />
      <path
        d="M-94.098 73.19V49.14h144.47v47.84h-144.47V73.19Z"
        stroke="#1C1D1C"
        strokeWidth={3.62}
        strokeMiterlimit={10}
      />
      <path
        d="M-94.238 73.064s.09.09.14.12c7.26 6.82 21.51 6.78 28.66-.12 7.21-6.95 21.61-6.95 28.8 0 7.21 6.95 21.61 6.95 28.8 0 7.21-6.95 21.61-6.95 28.82 0 7.2 6.95 21.59 6.95 28.8 0"
        stroke="#1C1D1C"
        strokeWidth={3.62}
        strokeMiterlimit={1}
      />
      <path
        d="M107.241 82.013h18.43l-7.83-7.83 7.37-7.37h-18.5"
        fill="#E83F37"
      />
      <path
        d="M107.241 82.013h18.43l-7.83-7.83 7.37-7.37h-18.5"
        stroke="#000"
        strokeWidth={3.62}
        strokeMiterlimit={10}
      />
      <path
        d="M70.828 42.86c20.54 0 37.18 14.12 37.18 31.55s-16.65 31.549-37.18 31.549-37.18-14.12-37.18-31.55 16.65-31.55 37.18-31.55Z"
        fill="#FDE8DE"
      />
      <path
        d="M70.828 105.959c20.534 0 37.18-14.125 37.18-31.55 0-17.424-16.646-31.55-37.18-31.55s-37.18 14.126-37.18 31.55c0 17.425 16.646 31.55 37.18 31.55Z"
        stroke="#1C1D1C"
        strokeWidth={3.62}
        strokeMiterlimit={10}
      />
    </g>
  </svg>
);

export default Snake3;

export function WhySponsorPage({
  whySponsor,
}: {
  whySponsor: { introduction: string; text: string };
}) {
  return (
    <div className="page bg-cream flex flex-col gap-[1cm] p-[2cm] relative h-screen">
      <h1 className="text-xl font-bold">Why sponsor PyCon Italia?</h1>

      <div className="flex flex-col gap-[1cm] justify-between h-full">
        <p className="bg-purple border-4 border-black px-[1cm] py-[0.5cm] w-[45%]">
          {compile(whySponsor.introduction).tree}
        </p>

        <div className="flex justify-between">
          <Snake1 className="size-[4cm] border-black border-4 bg-blue translate-y-32" />
          <Snake2 className="size-[4cm] border-black border-4 bg-[#6779BA]" />
          <Snake3 className="size-[4cm] border-black border-4 bg-yellow -translate-y-32" />
        </div>

        <p className="bg-pink border-4 border-black px-[0.5cm] py-[0.5cm] w-[50%] self-end">
          {compile(whySponsor.text).tree}
        </p>
      </div>
    </div>
  );
}
