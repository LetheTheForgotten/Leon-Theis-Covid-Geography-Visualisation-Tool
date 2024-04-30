import { Component } from '@angular/core';
import { BaseDataServiceService } from '../Services/BaseDataService/base-data-service.service';
import { ComparisonServiceService } from '../Services/ComparisonService/comparison-service.service';
import { HttpClient } from '@angular/common/http';
import { MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-msa-popup',
  templateUrl: './msa-popup.component.html',
  styleUrl: './msa-popup.component.css'
})
export class MSAPopupComponent {
  MSAState: boolean;
  MSAtimeout: number;
  environment = environment;
  constructor(private BDSS: BaseDataServiceService, private CS: ComparisonServiceService, private http: HttpClient, public dialogRef: MatDialogRef<MSAPopupComponent>, private snackBar: MatSnackBar) {
    this.MSAtimeout = 0;
    this.MSAState = BDSS.getMSAState();
  }

  submitMSA() {
    if (this.BDSS.getSeqDataSetSelected().length > 1) {
      this.CS.multipleSequenceAlignment(this.MSAtimeout);
      this.MSAState = false;
      this.BDSS.setMSAState(false);
    }
    else {
      this.snackBar.open("less than two sequences are selected", "dismiss")
    }
  }

}
