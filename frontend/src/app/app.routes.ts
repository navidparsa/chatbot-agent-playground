import {Routes} from '@angular/router';
import {Chat} from './pages/chat/chat';
import {SmartHome} from './pages/smart-home/smart-home';

export const routes: Routes = [
  { path: '',      component: Chat},
  { path: 'smart-home', component: SmartHome },
];
