import {
  Button,
  CardPart,
  Grid,
  Heading,
  HorizontalStack,
  Input,
  MultiplePartsCard,
  Spacer,
  Text,
  VerticalStack,
} from "@python-italia/pycon-styleguide";
import { useCallback } from "react";
import { FormattedMessage } from "react-intl";
import type { FormState, Inputs, StateErrors } from "react-use-form-state";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import type { CfpFormQuery } from "~/types";
import type { CfpFormFields, GetErrorsKey, SubmissionStructure } from ".";
import { FileInput } from "../file-input";

type Props = {
  conferenceData: CfpFormQuery;
  formState: FormState<CfpFormFields, StateErrors<CfpFormFields>>;
  formOptions: Inputs<CfpFormFields>;
  getErrors: (field: GetErrorsKey) => any;
  submission: SubmissionStructure;
};

export const MaterialsSection = ({
  formState,
  getErrors,
  formOptions,
  submission,
}: Props) => {
  const materials = formState.values.materials ?? [];

  const onAddFile = useCallback(
    (e) => {
      e.preventDefault();
      if (materials.length >= 3) {
        return;
      }

      const newMaterials = [
        ...materials,
        {
          type: "file",
        },
      ];
      formState.setField("materials", newMaterials);
    },
    [formState, materials],
  );

  const onAddURL = useCallback(
    (e) => {
      e.preventDefault();
      if (materials.length >= 3) {
        return;
      }

      const newMaterials = [
        ...materials,
        {
          type: "link",
        },
      ];
      formState.setField("materials", newMaterials);
    },
    [formState, materials],
  );

  const inputPlaceholder = useTranslatedMessage("input.placeholder");

  return (
    <MultiplePartsCard>
      <CardPart contentAlign="left">
        <Heading size={3}>
          <FormattedMessage id="cfp.materials.title" />
        </Heading>
      </CardPart>

      <CardPart background="milk" contentAlign="left">
        <Text size={3}>
          <FormattedMessage id="cfp.materials.description" />
        </Text>
        <Spacer size="medium" />
        <Grid cols={1} gap="medium">
          {materials.map((material, index) => (
            <HorizontalStack gap="medium" alignItems="center" key={index}>
              <div className="w-full">
                {material.type === "file" ? (
                  <FileInput
                    name={`materials.${index}.file`}
                    type="proposal_material"
                    errors={
                      getErrors("validationMaterials")?.[index]?.fileId ?? []
                    }
                    accept="*/*"
                    value={material.fileId}
                    onChange={(fileId, info) => {
                      const newMaterials = [...materials];
                      newMaterials[index].fileId = fileId;
                      newMaterials[index].name = info?.name;
                      formState.setField("materials", newMaterials);
                    }}
                    fileAttributes={{
                      proposalId: submission?.id,
                    }}
                    showPreview={false}
                    currentFileName={material.name}
                  />
                ) : (
                  <Input
                    name={`materials.${index}.url`}
                    type="url"
                    placeholder={inputPlaceholder}
                    errors={
                      getErrors("validationMaterials")?.[index]?.url ?? []
                    }
                    value={material.url ?? ""}
                    onChange={(e) => {
                      const newMaterials = [...materials];
                      newMaterials[index].url = e.target.value;
                      newMaterials[index].name = e.target.value;
                      formState.setField("materials", newMaterials);
                    }}
                  />
                )}
              </div>
              <div>
                <Button
                  size="small"
                  variant="secondary"
                  background="red"
                  onClick={(e) => {
                    e.preventDefault();
                    const newMaterials = [...materials];
                    newMaterials.splice(index, 1);
                    formState.setField("materials", newMaterials);
                  }}
                >
                  <FormattedMessage id="cfp.materials.remove" />
                </Button>
              </div>
            </HorizontalStack>
          ))}
          <HorizontalStack gap="medium" alignItems="center">
            <Text size={3}>
              <FormattedMessage id="cfp.materials.add" />
            </Text>
            <Button
              size="small"
              onClick={onAddFile}
              disabled={materials.length >= 3}
            >
              <FormattedMessage id="cfp.materials.addFile" />
            </Button>
            <Button
              size="small"
              onClick={onAddURL}
              disabled={materials.length >= 3}
            >
              <FormattedMessage id="cfp.materials.addURL" />
            </Button>
          </HorizontalStack>
        </Grid>
      </CardPart>
    </MultiplePartsCard>
  );
};
