import {
  FileInput as FileInputUI,
  HorizontalStack,
  Spacer,
  Text,
  VerticalStack,
} from "@python-italia/pycon-styleguide";
import clsx from "clsx";

import React, { type ChangeEvent, useRef, useState } from "react";
import { FormattedMessage } from "react-intl";

import {
  getTranslatedMessage,
  useTranslatedMessage,
} from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import { useFinalizeUploadMutation, useUploadFileMutation } from "~/types";

const MAX_UPLOAD_SIZE_IN_MB = 1 * 1024 * 1024;

export const FileInput = ({
  onChange: baseOnChange,
  name,
  value,
  errors = null,
  type,
  previewUrl,
  accept,
  fileAttributes,
  showPreview = true,
  currentFileName,
}: {
  onChange: (value: string, info?: { name?: string }) => void;
  name: string;
  value: string;
  errors?: string[];
  type: "participant_avatar" | "proposal_material";
  previewUrl?: string;
  accept: string;
  fileAttributes?: Record<string, string>;
  showPreview?: boolean;
  currentFileName?: string;
}) => {
  const conferenceCode = process.env.conferenceCode;
  const canvas = useRef<HTMLCanvasElement>(undefined);
  const language = useCurrentLanguage();

  const [uploadFile] = useUploadFileMutation();
  const [finalizeUpload] = useFinalizeUploadMutation();

  const [filePreview, setFilePreview] = useState<string | null>(previewUrl);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const resetInput = (triggerOnChange = true) => {
    setError("");

    if (filePreview) {
      URL.revokeObjectURL(filePreview);
      if (triggerOnChange) {
        baseOnChange(null);
      }
    }

    setFilePreview(null);
  };

  const onChange = (file: File) => {
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

    resetInput(false);
    setSelectedFile(file);

    if (file.type.startsWith("image/")) {
      const fakeImg = document.createElement("img");
      fakeImg.onload = () => onImageLoaded(fakeImg, file);
      fakeImg.src = URL.createObjectURL(file);
    } else {
      startUploadFlow(file);
    }
  };

  const onImageLoaded = (image: HTMLImageElement, fileInfo: File) => {
    // convert the image to jpeg
    // in the future this could do more (resize etc)
    const context = canvas.current.getContext("2d");
    canvas.current.width = image.width;
    canvas.current.height = image.height;
    context.drawImage(image, 0, 0);
    canvas.current.toBlob(
      (blob) => {
        const file = new File([blob], `${fileInfo.name.split(".")[0]}.jpg`, {
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
          ...fileAttributes,
        },
      };
    } else if (type === "proposal_material") {
      input = {
        proposalMaterial: {
          conferenceCode,
          filename: file.name,
          ...fileAttributes,
        },
      };
    }

    try {
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

      baseOnChange(fileId, {
        name: file.name,
      });
    } catch (e) {
      const baseMessage = getTranslatedMessage(
        "fileInput.uploadFailed",
        language,
      );
      setError(`${baseMessage}: ${e.message}`);
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

      <Text size="label3">
        {isUploading && <FormattedMessage id="fileInput.uploading" />}
        {!isUploading && !showPreview && currentFileName && (
          <FormattedMessage
            id="fileInput.currentFile"
            values={{
              name: currentFileName,
            }}
          />
        )}
      </Text>

      {previewAvailable && showPreview && (
        <img
          className="h-52 mt-3"
          alt="Selection preview"
          src={previewAvailable}
        />
      )}

      <canvas ref={canvas} className="hidden" />
    </div>
  );
};
