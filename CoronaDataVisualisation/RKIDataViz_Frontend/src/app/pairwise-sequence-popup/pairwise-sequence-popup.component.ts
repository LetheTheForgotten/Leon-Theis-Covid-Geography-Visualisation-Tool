import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { ComparisonServiceService } from '../Services/ComparisonService/comparison-service.service';
import { BaseDataServiceService } from '../Services/BaseDataService/base-data-service.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-pairwise-sequence-popup',
  templateUrl: './pairwise-sequence-popup.component.html',
  styleUrl: './pairwise-sequence-popup.component.css'
})
export class PairwiseSequencePopupComponent {
  matchScore: number;
  gapPenalty: number;
  mismatchScore: number;
  extensionPenalty: number;
  showAlign: boolean;
  sequenceAlignState: boolean;
  moreThanTwo: boolean;
  environment = environment;

  constructor(private BDSS: BaseDataServiceService, private CS: ComparisonServiceService, private http: HttpClient, public dialogRef: MatDialogRef<PairwiseSequencePopupComponent>, private snackBar: MatSnackBar) {
    this.matchScore = 1;
    this.gapPenalty = -1;
    this.mismatchScore = 0;
    this.extensionPenalty = 0;
    this.showAlign = false;
    this.sequenceAlignState = this.BDSS.getSeqAlignState();
    this.moreThanTwo = this.BDSS.getSeqDataSetSelected().length > 2;
  }

  submitSequenceAlign() {
    if (this.BDSS.getSeqDataSetSelected().length > 1) {
      this.CS.PairWiseSequence(this.mismatchScore, this.matchScore, this.gapPenalty, this.extensionPenalty, this.showAlign);
      this.sequenceAlignState = false;
      this.BDSS.setSeqAlignState(false);
    }
    else {
      this.snackBar.open("less than two sequences are selected", "dismiss")
    }
  }

}
