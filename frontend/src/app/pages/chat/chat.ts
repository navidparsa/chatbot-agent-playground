import {AfterViewChecked, Component, ElementRef, signal, ViewChild} from '@angular/core';
import {ChatService} from '../../chat-service';
import {Message} from '../../message';

@Component({
  selector: 'app-chat',
  imports: [],
  templateUrl: './chat.html',
  styleUrl: './chat.css',
})
export class Chat implements AfterViewChecked{
  @ViewChild('scrollContainer') private scrollContainer!: ElementRef;

  messages = signal<Message[]>([]);
  input = signal('');
  isStreaming = signal(false);
  models = signal<string[]>([]);
  selectedModel = signal('');

  constructor(private chat: ChatService) {
    this.chat.getModels().subscribe(list => {
      this.models.set(list);
      this.selectedModel.set(list[0] ?? '');
    });
  }

  ngAfterViewChecked() {
    const el = this.scrollContainer?.nativeElement;
    if (el) el.scrollTop = el.scrollHeight;
  }

  setInput(val: string) { this.input.set(val); }

  send() {
    const text = this.input().trim();
    if (!text || this.isStreaming()) return;

    this.messages.update(m => [...m, { role: 'user', content: text }]);
    this.input.set('');
    this.isStreaming.set(true);

    this.messages.update(m => [...m, { role: 'assistant', content: '' }]);

    this.chat.chat(this.messages().slice(0, -1), this.selectedModel()).subscribe({
      next: chunk => {
        this.messages.update(msgs => {
          const updated = [...msgs];
          updated[updated.length - 1] = {
            ...updated[updated.length - 1],
            content: updated[updated.length - 1].content + chunk
          };
          return updated;
        });
      },
      complete: () => this.isStreaming.set(false),
      error: () => this.isStreaming.set(false)
    });
  }

  onKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); this.send(); }
  }
}
