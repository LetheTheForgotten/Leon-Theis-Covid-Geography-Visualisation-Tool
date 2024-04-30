import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

declare let Plotly: any;
@Injectable({
  providedIn: 'root'
})
export class PlotlyService {
  isGraphPresent: boolean;

  constructor(private http: HttpClient) {
    this.isGraphPresent = false;
  }

  plot(input: any, divID: string) {
    this.purge(divID)
    this.isGraphPresent = true;

    Plotly.newPlot(divID, input.data, input.layout)
  }


  purge(divID: string) {
    if (this.isGraphPresent) {
      Plotly.purge(divID);
      this.isGraphPresent = false;
    }

  }

  plotLine(title: string, plotDiv: string, x: number[], y: number[]) {
    let trace = {
      x: x,
      y: y,
      type: 'scatter'
    };

    let layout = {
      title: title
    };

    Plotly.newPlot(plotDiv, [trace], layout);
  }
}
