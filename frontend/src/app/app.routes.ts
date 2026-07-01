import {Routes} from '@angular/router';
import {SmartHome} from './pages/smart-home/smart-home';

export const routes: Routes = [
  { path: '', component: SmartHome },
  { path: 'smart-home', component: SmartHome },
];
