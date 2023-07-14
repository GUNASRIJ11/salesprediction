import { Component, ViewChild, TemplateRef } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'client';

  @ViewChild('aboutUsDialog') aboutUsDialog!: TemplateRef<any>;

  constructor(private dialog: MatDialog) { }

  openAboutUsDialog(): void {
    this.dialog.open(this.aboutUsDialog);
  }

  closeAboutUsDialog(): void {
    this.dialog.closeAll();
  }
}
