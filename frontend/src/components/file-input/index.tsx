import {
  FileInput as FileInputUI,
  Text,
} from "@python-italia/pycon-styleguide";

import React, { type ChangeEvent, useRef, useState } from "react";
import { FormattedMessage } from "react-intl";

import {
  getTranslatedMessage,
  useTranslatedMessage,
} from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import { useFinalizeUploadMutation, useUploadFileMutation } from "~/types";

import { ErrorsList } from "../errors-list";

const MAX_UPLOAD_SIZE_IN_MB = 1 * 1024 * 1024;

export const FileInput = ({
  onChange: baseOnChange,
  name,
  value,
  errors = null,
  type,
  previewUrl,
  accept,
}: {
  onChange: (value: string) => void;
  name: string;
  value: string;
  errors?: string[];
  type: "participant_avatar" | "proposal_material";
  previewUrl?: string;
  accept: string;
}) => {
  const conferenceCode = process.env.conferenceCode;
  const canvas = useRef<HTMLCanvasElement>();
  const language = useCurrentLanguage();

  const [uploadFile] = useUploadFileMutation();
  const [finalizeUpload] = useFinalizeUploadMutation();

  const [filePreview, setFilePreview] = useState<string | null>(previewUrl);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const resetInput = () => {
    setError("");

    if (filePreview) {
      URL.revokeObjectURL(filePreview);
      baseOnChange(null);
    }

    setFilePreview(null);
  };

  const onChange = (file: File) => {
    setSelectedFile(file);
    console.log("file", file);

    if (!file) {
      resetInput();
      return;
    }

    if (file.size > MAX_UPLOAD_SIZE_IN_MB) {
      resetInput();
      setError(getTranslatedMessage("fileInput.fileSize", language));

      setSelectedFile(null);
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
    if (type === "participant_avatar") {
      input = {
        participantAvatar: {
          conferenceCode,
          filename: file.name,
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

      const fileId = response.id;
      await finalizeUpload({
        variables: {
          input: {
            fileId,
          },
        },
      });

      baseOnChange(fileId);
    } catch (e) {
      setError(getTranslatedMessage("fileInput.uploadFailed", language));
    } finally {
      setIsUploading(false);
    }
  };

  const previewAvailable = filePreview || previewUrl;
  const placeholder = useTranslatedMessage("fileInput.placeholder");
  const allErrors = error ? [error] : errors;

  return (
    <div>
      <FileInputUI
        placeholder={placeholder}
        onChange={onChange}
        name={name}
        accept={accept}
        value={selectedFile}
        errors={allErrors}
      />

      <canvas ref={canvas} className="hidden" />

      {isUploading && (
        <Text color="blue" size="label3">
          <FormattedMessage id="fileInput.uploading" />
        </Text>
      )}

      {previewAvailable && (
        <img
          className="h-52 mt-3"
          alt="Selection preview"
          src={previewAvailable}
        />
      )}
    </div>
  );
};
