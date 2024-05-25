import React, { type ChangeEvent, useRef, useState } from "react";
import { FormattedMessage } from "react-intl";

import { getTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import {
  useGenerateParticipantAvatarUploadUrlMutation,
  useUploadFileMutation,
} from "~/types";

import { Alert } from "../alert";
import { ErrorsList } from "../errors-list";

const MAX_UPLOAD_SIZE_IN_MB = 1 * 1024 * 1024;

export const FileInput = ({
  onChange: baseOnChange,
  name,
  onBlur,
  value,
  errors = null,
  purpose,
}: {
  onChange: (value: string) => void;
  name: string;
  onBlur: () => void;
  value: string;
  errors?: string[];
  purpose: "participant_avatar" | "proposal_resource";
}) => {
  const conferenceCode = process.env.conferenceCode;
  const fileInput = useRef<HTMLInputElement>();
  const canvas = useRef<HTMLCanvasElement>();
  const language = useCurrentLanguage();

  const [generateParticipantAvatarUploadUrl] =
    useGenerateParticipantAvatarUploadUrlMutation();

  const [uploadFile] = useUploadFileMutation();

  const [filePreview, setFilePreview] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState("");

  const resetInput = () => {
    setError("");

    if (filePreview) {
      URL.revokeObjectURL(filePreview);
      baseOnChange(null);
    }

    setFilePreview(null);
  };

  const onChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files[0];

    if (!file) {
      resetInput();
      return;
    }

    if (file.size > MAX_UPLOAD_SIZE_IN_MB) {
      resetInput();
      setError(getTranslatedMessage("fileInput.fileSize", language));

      fileInput.current.value = "";
      return;
    }

    resetInput();
    const fakeImg = document.createElement("img");
    fakeImg.onload = () => onImageLoaded(fakeImg);
    fakeImg.src = URL.createObjectURL(file);
  };

  const onImageLoaded = (image: HTMLImageElement) => {
    // convert the image to jpeg
    // in the future this could do more (resize etc)
    const context = canvas.current.getContext("2d");
    canvas.current.width = image.width;
    canvas.current.height = image.height;
    context.drawImage(image, 0, 0);
    canvas.current.toBlob(
      (blob) => {
        const file = new File([blob], "converted.jpg", {
          type: "application/octet-stream",
        });
        setFilePreview(URL.createObjectURL(file));
        startUploadFlow(file);
      },
      "image/jpeg",
      0.9,
    );
  };

  const startUploadFlow = async (file) => {
    setIsUploading(true);

    let input = {};
    console.log("purpose", purpose);
    if (purpose === "participant_avatar") {
      input = {
        participantAvatar: {
          conferenceCode,
        },
      };
    }

    const { data, errors } = await uploadFile({
      variables: {
        input,
      },
    });

    const response = data.uploadFile;

    if (errors || response.__typename !== "FileUploadRequest") {
      setError(getTranslatedMessage("fileInput.uploadFailed", language));
      return;
    }

    const uploadUrl = response.uploadUrl;
    const uploadFields = JSON.parse(response.fields);
    try {
      const formData = new FormData();
      Object.keys(uploadFields).forEach((key) => {
        formData.append(key, uploadFields[key]);
      });
      formData.append("file", file);

      const uploadRequest = await fetch(uploadUrl, {
        method: "POST",
        body: formData,
      });

      if (uploadRequest.status !== 204) {
        setError(getTranslatedMessage("fileInput.uploadFailed", language));
        return;
      }

      baseOnChange(response.id);
    } catch (e) {
      setError(getTranslatedMessage("fileInput.uploadFailed", language));
    } finally {
      setIsUploading(false);
    }
  };

  const previewAvailable = filePreview || value;

  return (
    <div>
      <input
        ref={fileInput}
        onChange={onChange}
        name={name}
        onBlur={onBlur}
        type="file"
        accept="image/png,image/jpg,image/jpeg,image/webp"
        className="w-full"
      />

      <canvas ref={canvas} className="hidden" />
      {(error || errors) && (
        <ErrorsList className="mt-2" errors={[error, ...(errors || [])]} />
      )}

      {previewAvailable && (
        <img
          className="h-52 mt-3"
          alt="Selection preview"
          src={previewAvailable}
        />
      )}

      {isUploading && (
        <Alert variant="info">
          <FormattedMessage id="fileInput.uploading" />
        </Alert>
      )}
    </div>
  );
};
