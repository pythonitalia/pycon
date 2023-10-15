/** @jsxRuntime classic */

/** @jsx jsx */
import React, { ChangeEvent, useRef, useState } from "react";
import { FormattedMessage } from "react-intl";
import { Box, jsx } from "theme-ui";

import { getTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import { useGenerateParticipantAvatarUploadUrlMutation } from "~/types";

import { Alert } from "../alert";
import { ErrorsList } from "../errors-list";

const MAX_UPLOAD_SIZE_IN_MB = 1 * 1024 * 1024;

export const FileInput = ({
  onChange: baseOnChange,
  name,
  onBlur,
  value,
  errors,
}) => {
  const fileInput = useRef<HTMLInputElement>();
  const canvas = useRef<HTMLCanvasElement>();
  const language = useCurrentLanguage();

  const [generateParticipantAvatarUploadUrl] =
    useGenerateParticipantAvatarUploadUrlMutation();

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

    const { data, errors } = await generateParticipantAvatarUploadUrl();

    if (errors) {
      setError(getTranslatedMessage("fileInput.uploadFailed", language));
      return;
    }

    const uploadUrl = data.generateParticipantAvatarUploadUrl.uploadUrl;
    try {
      const uploadRequest = await fetch(uploadUrl, {
        method: "PUT",
        headers: {
          // eslint-disable-next-line @typescript-eslint/ban-ts-comment
          // @ts-ignore
          "x-ms-blob-type": "BlockBlob",
          "Content-Type": "image/jpg",
        },
        body: file,
      });

      if (uploadRequest.status !== 201) {
        setError(getTranslatedMessage("fileInput.uploadFailed", language));
        return;
      }

      baseOnChange(data.generateParticipantAvatarUploadUrl.fileUrl);
    } catch (e) {
      setError(getTranslatedMessage("fileInput.uploadFailed", language));
    } finally {
      setIsUploading(false);
    }
  };

  const previewAvailable = filePreview || value;

  return (
    <Box>
      <input
        ref={fileInput}
        onChange={onChange}
        name={name}
        onBlur={onBlur}
        type="file"
        accept="image/png,image/jpg,image/jpeg,image/webp"
        sx={{
          width: "100%",
        }}
      />

      <canvas
        ref={canvas}
        sx={{
          display: "none",
        }}
      />
      {(error || errors) && (
        <ErrorsList sx={{ mt: 2 }} errors={[error, ...errors]} />
      )}

      {previewAvailable && (
        <img
          sx={{
            height: "200px",
            mt: 3,
          }}
          src={previewAvailable}
        />
      )}

      {isUploading && (
        <Alert variant="info">
          <FormattedMessage id="fileInput.uploading" />
        </Alert>
      )}
    </Box>
  );
};
