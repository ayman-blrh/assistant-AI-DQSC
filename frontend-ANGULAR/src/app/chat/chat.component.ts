import { CommonModule, NgFor, NgIf } from '@angular/common';
import { AfterViewChecked, Component, ElementRef, ViewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Reponse } from '../../const/const';
import { ChatService } from './chat.service';
import { AppComponent } from '../app.component';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.css',
  imports: [CommonModule, FormsModule, NgIf, NgFor]
})
export class ChatComponent implements AfterViewChecked {
  chatVisible = false;
  userMessage : string = '';
  error: string | null = null ;
  messages: { sender: 'user' | 'bot', text: string }[] = [];

  constructor(private chatService: ChatService , private app : AppComponent) {}
  @ViewChild('chatMessage') 
  private chatMessage!: ElementRef;
  isAdmin = true

  showChat() {
    this.chatVisible = true;
  }

  hideChat() {
    this.chatVisible = false;
  }

  addfile() {
    this.app.ouvrirModal()
  }

  sendMessage() {
    if(!this.userMessage.trim())
      return;

    this.messages.push({ sender: 'user', text: this.userMessage });
    this.error= null ;
    const msg = this.userMessage ;
    this.userMessage='';  
    this.chatService.sendMessage(msg).subscribe({
      next: (res : Reponse) => {
        this.messages.push({ sender: 'bot', text: res.answer });
      },
      error: err => {
        this.error=`Erreur : ${err.status || 'reseau'} ${err.statusText}`
      }
    })
  }

  ngAfterViewChecked(): void {
  this.scrollToBottom();
  }

  private scrollToBottom(): void {
  try {
    this.chatMessage.nativeElement.scrollTop = this.chatMessage.nativeElement.scrollHeight;
  } catch (err) {}
}

}
