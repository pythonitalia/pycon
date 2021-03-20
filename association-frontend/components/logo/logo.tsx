import classnames from "classnames";

type LogoProps = {
  className?: string;
};
const Logo = ({ className }: LogoProps) => {
  return (
    <svg
      viewBox="0 0 214.70 82.55"
      className={classnames(
        "text-blue-500 fill-current group-hover:text-blue-400",
        className,
      )}
      data-reactid="4"
    >
      <path
        d="M100.43 11.62v-.09c0-6.07-4.58-9.77-11.53-9.77h-9.81a1.76 1.76 0 0 0-1.72 1.76V31a1.74 1.74 0 1 0 3.48 0v-9.3h7.48c6.56 0 12.1-3.43 12.1-10.08zM80.85 5h7.79c5 0 8.27 2.29 8.27 6.69v.09c0 4-3.34 6.78-8.45 6.78h-7.61zm31.75 27.35l-.18.35c-1.23 2.77-2.46 4-4.58 4a7 7 0 0 1-2.46-.4 2.58 2.58 0 0 0-.84-.18 1.46 1.46 0 0 0-1.45 1.45 1.55 1.55 0 0 0 1.06 1.45 10.7 10.7 0 0 0 3.74.66c3.43 0 5.63-1.72 7.61-6.42l8.89-21.21a2.81 2.81 0 0 0 .18-.84 1.67 1.67 0 0 0-1.67-1.61 1.7 1.7 0 0 0-1.63 1.28l-7 17.91-7.92-17.87a1.8 1.8 0 0 0-1.72-1.32 1.68 1.68 0 0 0-1.72 1.67 2.37 2.37 0 0 0 .22.92zm28-1.32a1.47 1.47 0 0 0-1.45-1.45 9.59 9.59 0 0 1-2.07.31c-2.29 0-3.83-1-3.83-3.78v-13.3h5.9a1.52 1.52 0 0 0 1.54-1.5 1.55 1.55 0 0 0-1.54-1.5h-5.9V4.45a1.75 1.75 0 0 0-1.72-1.72 1.68 1.68 0 0 0-1.67 1.72v5.37H128a1.51 1.51 0 0 0-1.5 1.5 1.54 1.54 0 0 0 1.5 1.5h1.85v13.72c0 4.62 2.77 6.43 6.42 6.43a8.57 8.57 0 0 0 3.34-.62 1.41 1.41 0 0 0 1-1.35zm14.18-21.7a8.62 8.62 0 0 0-7.78 4.45V1.94a1.69 1.69 0 1 0-3.39 0v29.14a1.69 1.69 0 0 0 1.72 1.72 1.65 1.65 0 0 0 1.67-1.72V19.55c0-4.27 2.9-7.13 6.82-7.13s6.29 2.64 6.29 6.87v11.79a1.69 1.69 0 1 0 3.39 0V18.45c0-5.45-3.21-9.11-8.71-9.11zm24.17 0a11.78 11.78 0 0 0-11.88 11.88v.09a11.66 11.66 0 0 0 11.8 11.8 11.81 11.81 0 0 0 11.93-11.88v-.09A11.69 11.69 0 0 0 179 9.34zm8.36 12c0 4.8-3.43 8.76-8.36 8.76a8.53 8.53 0 0 1-8.41-8.84v-.09c0-4.8 3.39-8.8 8.32-8.8a8.61 8.61 0 0 1 8.45 8.89zm18.48-12a8.62 8.62 0 0 0-7.79 4.45v-2.46a1.69 1.69 0 0 0-1.72-1.72 1.71 1.71 0 0 0-1.67 1.72v19.76a1.69 1.69 0 0 0 1.72 1.72 1.65 1.65 0 0 0 1.67-1.72V19.55c0-4.27 2.9-7.13 6.82-7.13s6.29 2.64 6.29 6.87v11.79a1.69 1.69 0 1 0 3.39 0V18.45c.01-5.45-3.2-9.11-8.7-9.11zM79 48.58a1.17 1.17 0 0 0-1.14 1.14V78.6a1.14 1.14 0 0 0 2.29 0V49.73A1.17 1.17 0 0 0 79 48.58zM96.79 59.1a1 1 0 0 0 1-1 1.05 1.05 0 0 0-1-1h-7v-6.23a1.09 1.09 0 0 0-1.1-1.1 1.05 1.05 0 0 0-1.06 1.1v6.25h-2.46a1 1 0 0 0-1 1 1.05 1.05 0 0 0 1 1h2.42V73.8c0 4.27 2.82 6.16 6.29 6.16a9.28 9.28 0 0 0 3.17-.57 1 1 0 0 0 .7-.92 1 1 0 0 0-1-1 9.41 9.41 0 0 1-2.55.44c-2.6 0-4.49-1.14-4.49-4.36V59.1zm12.57-2.33a17.39 17.39 0 0 0-7.36 1.67 1.1 1.1 0 0 0-.62 1 1.05 1.05 0 0 0 1 1 1.15 1.15 0 0 0 .48-.13 14.5 14.5 0 0 1 6.38-1.5c4.62 0 7.39 2.33 7.39 6.86v1a27 27 0 0 0-7.44-1c-5.81 0-9.81 2.64-9.81 7.31v.09c0 4.66 4.49 7 8.67 7a10.21 10.21 0 0 0 8.58-4.27v2.82a1.06 1.06 0 1 0 2.11 0V65.57a8.52 8.52 0 0 0-2.29-6.34c-1.63-1.63-4.05-2.46-7.09-2.46zm7.31 14.39c0 4.09-3.92 6.91-8.49 6.91-3.43 0-6.51-1.89-6.51-5.15v-.09c0-3.12 2.64-5.24 7.39-5.24a29.79 29.79 0 0 1 7.61 1zm8.72-23.9a1.05 1.05 0 0 0-1.06 1.1v30.28a1.06 1.06 0 0 0 1.1 1.1 1 1 0 0 0 1.06-1.1V48.36a1.09 1.09 0 0 0-1.1-1.1zm8.11.84a1.3 1.3 0 0 0-1.32 1.32v.75a1.3 1.3 0 0 0 1.32 1.32 1.33 1.33 0 0 0 1.36-1.32v-.75a1.33 1.33 0 0 0-1.37-1.32zm0 8.85a1.05 1.05 0 0 0-1.06 1.1v20.6a1.06 1.06 0 0 0 1.1 1.1 1 1 0 0 0 1.06-1.1V58a1.06 1.06 0 0 0-1.11-1.06zm15-.18a17.39 17.39 0 0 0-7.39 1.67 1.1 1.1 0 0 0-.62 1 1.05 1.05 0 0 0 1 1 1.15 1.15 0 0 0 .48-.13 14.5 14.5 0 0 1 6.38-1.5c4.62 0 7.39 2.33 7.39 6.86v1a27 27 0 0 0-7.44-1c-5.81 0-9.81 2.64-9.81 7.31v.09c0 4.66 4.49 7 8.67 7a10.21 10.21 0 0 0 8.58-4.27v2.82a1.06 1.06 0 1 0 2.11 0V65.57a8.52 8.52 0 0 0-2.29-6.34c-1.56-1.63-3.98-2.46-7.02-2.46zm7.31 14.39c0 4.09-3.92 6.91-8.49 6.91-3.43 0-6.51-1.89-6.51-5.15v-.09c0-3.12 2.64-5.24 7.39-5.24a29.79 29.79 0 0 1 7.61 1zM37.29 0A21.72 21.72 0 0 0 15.6 21.69v12.12a2.9 2.9 0 0 0 5.79 0V21.69a15.92 15.92 0 0 1 15.9-15.9 18.28 18.28 0 0 1 0 36.56H18.5A18.52 18.52 0 0 0 0 60.85v8.93a10.7 10.7 0 1 0 21.39 0V56.55a2.9 2.9 0 1 0-5.79 0v13.23a4.9 4.9 0 1 1-9.81 0v-8.93a12.72 12.72 0 0 1 12.7-12.7h18.8a24.07 24.07 0 0 0 0-48.15z"
        fill="white"
      ></path>
    </svg>
  );
};

export default Logo;
