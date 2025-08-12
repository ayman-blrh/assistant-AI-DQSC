import { NgIf } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IngestionService } from './ingestion.service';
import { Component, EventEmitter, Output } from '@angular/core';
import { HttpEventType } from '@angular/common/http';

@Component({
  selector: 'app-ingestion',
  imports:[NgIf,FormsModule],
  templateUrl: './ingestion.component.html',
  styleUrl: './ingestion.component.css'
})
export class IngestionComponent {
  selectedFile?: File;
  progress = 0;
  serverPath = '';
  isUploading = false;
  errorMsg = '';

  constructor(private uploadService: IngestionService) {}

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files && input.files[0];
    this.selectedFile = file || undefined;
    this.progress = 0;
    this.serverPath = '';
    this.errorMsg = '';
  }

  @Output() fermer = new EventEmitter<void>();

  fermerModal() {
    this.fermer.emit();
  }
  
  upload() {
    if (!this.selectedFile) {
      this.errorMsg = 'Veuillez sélectionner un fichier.';
      return;
    }
    this.isUploading = true;
    this.progress = 0;
    this.errorMsg = '';

    this.uploadService.upload(this.selectedFile).subscribe({
      next: (event) => {
        if (event.type === HttpEventType.UploadProgress && event.total) {
          this.progress = Math.round((100 * event.loaded) / event.total);
        } else if (event.type === HttpEventType.Response) {
          // On attend un JSON { path: "chemin/vers/fichier" }
          this.serverPath = event.body?.path ?? '';
          this.isUploading = false;
        }
      },
      error: (err) => {
        this.errorMsg = 'Échec de l’envoi du fichier.';
        this.isUploading = false;
      }
    });
  }

  reset() {
    this.selectedFile = undefined;
    this.progress = 0;
    this.serverPath = '';
    this.errorMsg = '';
  }
}
