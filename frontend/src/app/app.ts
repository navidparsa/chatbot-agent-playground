import {Component} from '@angular/core';
import {Sidebar} from './sidebar/sidebar';
import {RouterOutlet} from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  standalone: true,
  imports: [
    Sidebar,
    RouterOutlet
  ],
  styleUrl: './app.css'
})
export class Apps {

}





