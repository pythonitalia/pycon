export const displayAttendeeName = ({
  parts,
  scheme,
}: {
  parts: any;
  scheme: string;
}) => {
  switch (scheme) {
    case "given_family":
      return [parts.given_name, parts.family_name].join(" ");
    case "legacy":
      return parts._legacy;
    case "":
      return "";
    default:
      console.error(`Unknown attendee name scheme: ${scheme}`);
      break;
  }
};
