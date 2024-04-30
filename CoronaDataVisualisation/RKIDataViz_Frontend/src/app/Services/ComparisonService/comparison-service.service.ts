import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, interval, timer } from 'rxjs';
import { BaseDataServiceService } from '../BaseDataService/base-data-service.service';
import { persistentData } from '../../persistent-data/persistent-data';
import { environment } from './../../../environments/environment';


class graphRequest {
  data: any;
  operation: string;

  constructor(operationType: string, dataIn: any) {
    this.operation = operationType;
    this.data = dataIn;
  }
}


@Injectable({
  providedIn: 'root'
})

export class ComparisonServiceService {
  timerObject: any;

  Graph: persistentData<any>;

  timerSubscription: any;

  graphSubject: BehaviorSubject<boolean>;

  _isGraphObject: persistentData<boolean>;

  constructor(private http: HttpClient, private BDSS: BaseDataServiceService) {
    this.timerObject = timer(0, 5000);
    this.graphSubject = new BehaviorSubject<boolean>(false);

    //Graph causes update function on change -> be sure to update isGraphObject BEFORE updating graph every time
    this._isGraphObject = new persistentData<boolean>(false, "comparisonService.isGraphObject", (value: any) => { return; });
    this.Graph = new persistentData<any>(null, "comparisonService.Graph", (value: boolean) => this.graphSubject.next(false))
  }

  getGraphObject() {
    return this.Graph.get();
  }

  getGraphSubject() {
    return this.graphSubject;
  }

  isGraphObject() {
    return this._isGraphObject.get();
  }


  multipleSequenceAlignment(timeout: number) {
    var Seq = this.BDSS.getSeqDataSetSelected();
    var request = new graphRequest("multipleSequenceAlignment", {
      "Seq": Seq, "timeout": timeout
    });
    this.makeGraph(request);
  }

  pangolinPieChart(minCount: number, startDate: Date, endDate: Date, renkonen:boolean) {
    var PLZ = this.BDSS.getPLZDataSetSelected();
    var request = new graphRequest("pangolinPieChart", {
      "PLZ": PLZ,
      "startDate": startDate,
      "endDate": endDate,
      "minPercentage": minCount,
      "renkonen":renkonen
    });
    this.makeGraph(request);

  }

  PLZScatterPlotByPLZ(pangolinSelected: any, minSelected: number, startDate: Date, endDate: Date) {
    var PLZ = this.BDSS.getPLZDataSetSelected();
    var request = new graphRequest("PLZScatterPlotByPLZ", {
      "PLZ": PLZ,
      "pangolins": pangolinSelected,
      "minsamples": minSelected,
      "start": startDate,
      "end": endDate
    });
    this.makeGraph(request)
  }

  PLZScatterPlotByPangolin(pangolinSelected: any, minValue: any, startDate: Date, endDate: Date) {
    var PLZ = this.BDSS.getPLZDataSetSelected();
    var request = new graphRequest("PLZScatterPlotByPangolin", {
      "PLZ": PLZ,
      "pangolins": pangolinSelected,
      "minsamples": minValue,
      "start": startDate,
      "end": endDate

    });
    this.makeGraph(request)
  }

  PairWiseSequence(mismatchPenalty: number, matchScore: number, gapPenalty: number, extensionPenalty: number, showAlign: boolean) {
    var Seq = this.BDSS.getSeqDataSetSelected();
    var request = new graphRequest("pairWiseSequenceAlignment", {
      "Seq": Seq,
      "match": matchScore,
      "mismatch": mismatchPenalty,
      "gap": gapPenalty,
      "extension": extensionPenalty,
      "showAlign": showAlign
    }

    );
    this.makeGraph(request);
  }



  makeGraph(data: any) {

    this.Graph.set(null);

    this.graphSubject.next(false);
    this._isGraphObject.set(false);

    this.http.post(environment.CREATE_GRAPH_PATH, data, { observe: "response" }).subscribe({
      next: (response: any) => {

        if (response.statusText == environment.GRAPH_JOB_STARTED) {

          this.timerSubscription = this.timerObject.subscribe((n: any) => { this.getGraph() });
        }
        else {
          console.log("http post graph failed: job already running");
        }
      },
      error: (error: any) => console.log(error)
    });

  }

  getGraph() {
    this.http.get(environment.CHECK_GRAPH_SERVICE_STATUS_PATH, { observe: "response", responseType: "text" }).subscribe(
      {
        next: (response: any) => {

          //if job is still running do nothing
          if (response.statusText == environment.GRAPH_JOB_STILL_RUNNING) {
            this._isGraphObject.set(false);
            this.Graph.set(response.body);

            this.graphSubject.next(false);
            return;
          }
          //if job is not running or get graph resulted in error, unsubscribe from timer
          if (response.statusText == environment.GRAPH_NO_JOB_RUNNING || response.statusText == environment.GRAPH_GET_RESULT_ERROR) {
            this.timerSubscription.unsubscribe();
            return;
          }
          if (response.statusText == environment.GRAPH_JOB_DONE) {
            //angular doesn't accept variable response types, try parse solution 
            try {
              this._isGraphObject.set(true);
              this.Graph.set(JSON.parse(response.body));

            }
            catch (e) {
              this._isGraphObject.set(false);
              this.Graph.set(response.body);

            }
            this.graphSubject.next(false);

            this.timerSubscription.unsubscribe();
          }
          this.timerSubscription.unsubscribe();


        }
      }
    )
  }

}

