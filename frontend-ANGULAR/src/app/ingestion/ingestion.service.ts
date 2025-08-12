import { Injectable } from '@angular/core';
import { HttpClient, HttpEvent, HttpRequest } from '@angular/common/http';
import { Observable } from 'rxjs';
import { BASE_URL } from '../constant/const';


@Injectable({ providedIn: 'root' })
export class IngestionService {

  private baseUrl = BASE_URL + 'ingest';

  constructor(private http: HttpClient) {}

  upload(file: File): Observable<HttpEvent<any>> {
    
    const formData = new FormData();
    
    formData.append('file', file); 

    return this.http.post<any>(this.baseUrl,formData, {
        reportProgress: true,
        observe: 'events'
    })
  }
}
