import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Question, Reponse } from '../../const/const';

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  private apiUrl = 'http://localhost:8000/ask';

  constructor(private http: HttpClient) { }

  sendMessage(message: string) : Observable<Reponse>{
    const payload: Question = {
        question: message
    };
    const headers = new HttpHeaders({
      'Content-Type' : 'application/json'
    })
    return this.http.post<Reponse>(this.apiUrl,payload, { 
      headers,
      withCredentials:true 
    });
  }
}
