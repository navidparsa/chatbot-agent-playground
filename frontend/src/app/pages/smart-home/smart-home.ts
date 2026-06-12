import {Component, inject, OnInit, signal} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {FormsModule} from '@angular/forms';
import {ChatService} from '../../chat-service';

@Component({
  selector: 'app-smart-home',
  imports: [
    FormsModule
  ],
  templateUrl: './smart-home.html',
  styleUrl: './smart-home.css',
  standalone: true,
})
export class SmartHome  implements OnInit {

  LAPM_COUNT = 12;
  private chatService = inject(ChatService);
  ngOnInit(): void {
    this.chatService.getModels().subscribe(list => {
      this.models.set(list);
      this.selectedModel.set(list[0] ?? '');
    });
  }

  private http = inject(HttpClient);

  lamps = signal<number[]>(Array(this.LAPM_COUNT).fill(0));
  input = signal('');
  loading = signal(false);
  error = signal('');
  models = signal<string[]>([]);
  selectedModel = signal('llama3.1:8b');

  lampNumbers = Array.from({ length: this.LAPM_COUNT }, (_, i) => i + 1);

  send() {
    const msg = this.input().trim();
    if (!msg || this.loading()) return;

    this.loading.set(true);
    this.error.set('');

    this.http.post<{ states: number[]; error?: string }>('http://localhost:8000/smart-home/lamps', { message: msg,model: this.selectedModel() })
      .subscribe({
        next: (res) => {
          this.lamps.set(res.states);
          if (res.error) this.error.set(res.error);
          this.input.set('');this.loading.set(false);
        },
        error: () => {
          this.error.set('Failed to connect to backend.');
          this.loading.set(false);
        }
      });
  }

  onKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); this.send(); }
  }
}
