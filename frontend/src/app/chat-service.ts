import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {map, Observable} from 'rxjs';
import {Message} from './message';

@Injectable({
  providedIn: 'root',
})
export class ChatService {
  private api = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  getModels(): Observable<string[]> {
    return this.http.get<{models: string[]}>('http://localhost:8000/models')
      .pipe(map(r => r.models));
  }


  chat(messages: Message[], model: string): Observable<string> {
    return new Observable(observer => {
      fetch(`${this.api}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages, model })
      }).then(res => {
        const reader = res.body!.getReader();
        const decoder = new TextDecoder();

        const read = () => {
          reader.read().then(({ done, value }) => {
            if (done) { observer.complete(); return; }
            const lines = decoder.decode(value).split('\n');
            for (const line of lines) {
              if (line.startsWith('data: ')) {
                const data = line.slice(6);
                if (data === '[DONE]') { observer.complete(); return; }
                try {
                  const parsed = JSON.parse(data);
                  observer.next(parsed.content);
                } catch {}
              }
            }
            read();
          });
        };
        read();
      }).catch(err => observer.error(err));
    });
  }
}
