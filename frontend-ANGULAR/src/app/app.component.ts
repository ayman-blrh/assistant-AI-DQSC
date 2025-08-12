import { Component } from '@angular/core';
import { CommonModule, NgIf, NgFor } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService } from './chat/chat.service';
import { Question, Reponse } from '../const/const';
import { ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { ChatComponent } from './chat/chat.component';
import { IngestionComponent } from './ingestion/ingestion.component';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  imports: [ ChatComponent , IngestionComponent , NgIf]
})
export class AppComponent {
  modalVisible = false;

  ouvrirModal() {
    this.modalVisible = true;
  }

  fermerModal() {
    this.modalVisible = false;
  }
}