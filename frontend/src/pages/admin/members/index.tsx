import * as React from 'react';
import { RouteComponentProps } from '@reach/router';

import { Title } from '../../../components/title/index';

export const Members = (props: RouteComponentProps) => (
  <>
    <Title>Members list</Title>

    <table>
      <thead>
        <tr>
          <th>Nome</th>
          <th>Stato</th>
          <th>Scadenza</th>
          <th />
        </tr>
      </thead>

      <tbody>
        <tr>
          <td>Patrick Arminio</td>
          <td>Attivo</td>
          <td>20 aprile 2019</td>
        </tr>
      </tbody>
    </table>
  </>
);
