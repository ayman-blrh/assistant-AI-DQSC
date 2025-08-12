import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Pipe({ name: 'formatAnswer' })
export class FormatAnswerPipe implements PipeTransform {
  constructor(private sani: DomSanitizer) {}

  transform(text: string | null | undefined): SafeHtml {
    if (!text) return '';

    let t = text.trim();

    // listes numérotées (lignes commençant par "1. ", "2. ", …)
    const lines = t.split(/\n+/).map(l => l.trim()).filter(Boolean);

    const isNumbered = lines.filter(l => /^\d+\.\s+/.test(l)).length >= 2;
    const isBulleted = lines.filter(l => /^[•\-*]\s+/.test(l)).length >= 2;

    let html = '';

    if (isNumbered) {
      const items = lines.map(l => l.replace(/^\d+\.\s+/, '').trim());
      html = `<ol>${items.map(li => `<li>${this.escape(li)}</li>`).join('')}</ol>`;
    } else if (isBulleted) {
      const items = lines.map(l => l.replace(/^[•\-*]\s+/, '').trim());
      html = `<ul>${items.map(li => `<li>${this.escape(li)}</li>`).join('')}</ul>`;
    } else {
      // paragraphes/sauts de ligne
      html = this.escape(t).replace(/\n/g, '<br>');
    }

    return this.sani.bypassSecurityTrustHtml(html);
  }

  private escape(s: string) {
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
  }
}
