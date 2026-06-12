import {bootstrapApplication} from '@angular/platform-browser';
import {appConfig} from './app/app.config';
import { Apps } from "./app/app";

bootstrapApplication(Apps, appConfig)
  .catch((err) => console.error(err));
