import * as React from 'react';
import { RouteComponentProps } from '@reach/router';

import { Title } from '../../../components/title/index';
import { Card } from '../../../components/card/index';
import { Table } from '../../../components/table/index';

export const Members = (props: RouteComponentProps) => (
  <Card title="Members (10)">
    <Table
      columns={['Nome', 'Stato', 'Scadenza']}
      data={[
        { nome: 'Patrick', stato: 'Attivo', scadenza: '19 Febbraio 2019' },
        { nome: 'Patrick', stato: 'Attivo', scadenza: '19 Febbraio 2019' },
        { nome: 'Patrick', stato: 'Attivo', scadenza: '19 Febbraio 2019' },
        { nome: 'Patrick', stato: 'Attivo', scadenza: '19 Febbraio 2019' },
        { nome: 'Patrick', stato: 'Attivo', scadenza: '19 Febbraio 2019' },
      ]}
    />
  </Card>
);
