import { Component } from '@angular/core';
import { BaseDataServiceService, Modes } from '../Services/BaseDataService/base-data-service.service';
import { ComparisonServiceService } from '../Services/ComparisonService/comparison-service.service';
import { MatDialog } from '@angular/material/dialog';
import { TableComponent } from '../Elements/table/table.component';
import { PangolinLineagePopupComponent } from '../pangolin-lineage-popup/pangolin-lineage-popup.component';
import { PangolinLineagePopupSequenceBasedGraphComponent } from '../pangolin-lineage-popup-sequence-based-graph/pangolin-lineage-popup-sequence-based-graph.component';
import { SummaryPopupComponent } from '../summary-popup/summary-popup.component';
import { MSAPopupComponent } from '../msa-popup/msa-popup.component';
import { PairwiseSequencePopupComponent } from '../pairwise-sequence-popup/pairwise-sequence-popup.component';
import { HttpClient } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import { environment } from '../../environments/environment';
import { clearLocalStorage } from '../persistent-data/persistent-data';


@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrl: './main-page.component.css'
})
export class MainPageComponent {
  checked: boolean;
  graphVisible: boolean;
  mode: Modes;
  enum = Modes;
  fastaDownloading: boolean;
  environment = environment;

  constructor(private BDSS: BaseDataServiceService, private CS: ComparisonServiceService, public dialouge: MatDialog, private http: HttpClient, private snackBar: MatSnackBar) {
    this.graphVisible = true;
    this.mode = BDSS.getMode();
    this.checked = this.checkMode();
    this.fastaDownloading = !this.checkSeqSelected();

  }


  //--------------------Graph Pane Functions------------------------//

  setGraphInvis() {
    this.graphVisible = false;
  }

  setGraphVisible() {
    this.graphVisible = true;
  }



  //--------------------Table Mode Functions------------------------//

  checkMode() {
    if (this.mode == Modes.PostalCode) {
      return false;
    }
    if (this.mode == Modes.Sequence) {
      return true;
    }
    else {
      return false;
    }
  }

  changeMode(input: any) {
    if (input.checked == false) {
      this.mode = Modes.PostalCode;
    }
    if (input.checked == true) {
      this.mode = Modes.Sequence
    }
    this.BDSS.setMode(this.mode)
  }


  openTable() {
    const dialougeTable = this.dialouge.open(TableComponent, { height: "99%", width: "99%" })
  }


  //--------------------PLZ Mode Functions------------------------//

  openPangonlinPieDialouge() {
    const dialougeTable_pangolinPie = this.dialouge.open(SummaryPopupComponent, { height: "99%", width: "99%" })
  }

  openPLZScatterChartDialouge() {
    const dialougeTable = this.dialouge.open(PangolinLineagePopupComponent, { height: "99%", width: "99%" })
  }

  openLineageScatterChartDialouge() {
    const dialougeTable_lineage = this.dialouge.open(PangolinLineagePopupSequenceBasedGraphComponent, { height: "99%", width: "99%" })
  }


  //--------------------Sequence Mode Functions------------------------//


  openPairwiseDialouge() {
    const dialougeSA = this.dialouge.open(PairwiseSequencePopupComponent, { height: "50%", width: "38%" })
  }
  openMSADialouge() {
    const dialougeSelectMSA = this.dialouge.open(MSAPopupComponent, { height: "30%", width: "50%" })
  }

  downloadSequences() {
    if (this.checkSeqSelected()) {
      var seqData = this.BDSS.getSeqDataSetSelected()

        
      this.http.post(
        environment.DOWNLOAD_SELECTED_PATH, seqData).subscribe({
          next: (r: any) => { window.open(environment.DOWNLOAD_SELECTED_GETTER_PATH, "_blank") },
        error: (error: any) => console.log(error)
      })

    }
    else {
      this.snackBar.open("less than one sequence is selected", "dismiss")
    }



  }
  downloadMetaData() {
    if (this.checkSeqSelected()) {
      var seqData = this.BDSS.getSeqDataSetSelected()


      this.http.post(
        environment.DOWNLOAD_SELECTED_META_PATH, seqData).subscribe({
          next: (r: any) => { window.open(environment.DOWNLOAD_SELECTED_META_GETTER_PATH, "_blank") },
          error: (error: any) => console.log(error)
        })

    }
    else {
      this.snackBar.open("less than one sequence is selected", "dismiss")
    }



  }


  clearLocalStorage() {
    clearLocalStorage(this.http);

    
  }

  checkSeqSelected() {
    if (this.BDSS.getSeqDataSetSelected().length > 0) {
      return true;
    }
    else {
      return false;
    }
  }

  setModePLZ() {
    this.BDSS.setMode(Modes.PostalCode);

  }
  setModeSeq() {
    this.BDSS.setMode(Modes.Sequence);

  }


  title = 'RKIDataViz_Frontend';
}

