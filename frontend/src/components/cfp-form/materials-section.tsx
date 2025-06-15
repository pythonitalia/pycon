import {
  Button,
  CardPart,
  Grid,
  Heading,
  MultiplePartsCard,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import { useCallback } from "react";
import { FormattedMessage } from "react-intl";
import type { FormState, Inputs, StateErrors } from "react-use-form-state";
import type { CfpFormQuery } from "~/types";
import type { CfpFormFields } from ".";
import { FileInput } from "../file-input";

type Props = {
  conferenceData: CfpFormQuery;
  formState: FormState<CfpFormFields, StateErrors<CfpFormFields>>;
  formOptions: Inputs<CfpFormFields>;
  getErrors: (field: keyof CfpFormFields) => string[] | null;
};

export const MaterialsSection = ({
  conferenceData,
  formState,
  getErrors,
  formOptions,
}: Props) => {
  const { raw } = formOptions;
  const materials = formState.values.materials ?? [];

  const onAdd = useCallback(() => {
    const newMaterials = [...materials, {}];
    formState.setField("materials", newMaterials);
  }, [formState]);

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
        <Grid cols={1} gap="medium">
          {materials.map((material, index) => (
            <FileInput
              key={index}
              {...raw("materials")}
              type="proposal_material"
              errors={getErrors("materials")}
            />
          ))}
          <div>
            <Button size="small" onClick={onAdd}>
              <FormattedMessage id="cfp.materials.add" />
            </Button>
          </div>
        </Grid>
      </CardPart>
    </MultiplePartsCard>
  );
};
