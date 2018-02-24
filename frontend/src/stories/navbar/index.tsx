import React from 'react';
import { storiesOf } from '@storybook/react';

import { Navbar } from '../../components/navbar';

storiesOf('Navbar', module).add('normal', () => <Navbar />);
