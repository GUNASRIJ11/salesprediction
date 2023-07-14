import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-predict',
  templateUrl: './predict.component.html',
  styleUrls: ['./predict.component.scss']
})
export class PredictComponent {
  
  file!: File ;
  timePeriod!: string;
  
  constructor(private http: HttpClient) {}

  onFileSelected(event: any) {
    this.file = event.target.files[0];
  }

  
  
  ngOnInit(): void {}

  onSubmit() {
    const formData = new FormData();
    formData.append('file', this.file);
    formData.append('timePeriod', this.timePeriod);
    this.http.post('http://127.0.0.1:5000/predict_sales', formData).subscribe((data) => 
    console.log(data))
    
  }


}
