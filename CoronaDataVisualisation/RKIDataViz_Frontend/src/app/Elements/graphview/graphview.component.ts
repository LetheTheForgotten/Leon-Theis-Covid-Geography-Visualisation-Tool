import { Component, OnInit } from '@angular/core';
import { ComparisonServiceService } from '../../Services/ComparisonService/comparison-service.service';
import { PlotlyService } from '../../Services/PlotlyService/plotly.service';

@Component({
  selector: 'app-graphview',
  templateUrl: './graphview.component.html',
  styleUrl: './graphview.component.css'
})
export class GraphviewComponent implements OnInit {
  text: any;

  constructor(private CS: ComparisonServiceService, private PS: PlotlyService) {

  }

  ngOnInit() {
    this.CS.getGraphSubject().subscribe((result: any) => {
      this.updateGraph();
    }
    );
  }

  updateGraph() {
    if (this.CS.getGraphObject() == null) {
      return;
    }

    if (this.CS.isGraphObject()) {
      this.text = ""
      this.PS.plot(this.CS.getGraphObject(), "graph");
    }
    else {
      this.PS.purge("graph")
      this.text = this.CS.getGraphObject();
    }
  }
}
