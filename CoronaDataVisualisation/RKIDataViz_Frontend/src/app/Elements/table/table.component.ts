
import { AfterViewInit, ChangeDetectionStrategy, ChangeDetectorRef, Component, Optional, ViewChild } from '@angular/core';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { BaseDataServiceService, PLZElement, SeqElement, Modes } from '../../Services/BaseDataService/base-data-service.service';
import { MatPaginator } from '@angular/material/paginator';
import { AbstractControl, FormControl, ValidationErrors, ValidatorFn, Validators } from '@angular/forms';
import { MatDatepickerInputEvent } from '@angular/material/datepicker';
import { MatDialogRef } from '@angular/material/dialog';

export function acceptedPLZValidator(plzlist: any): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const accept = plzlist.includes(control.value);
    return accept ? null : { acceptedValue: { value: control.value } };
  };
}

export function forbiddenPLZValidator(activePLZList: any): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    var forbidden = false;
    if (activePLZList.has(control.value)) {
      forbidden = activePLZList.get(control.value);
    }

    return forbidden ? { forbiddenValue: { value: control.value } } : null;
  };
}
export const filterKeyword = "__FilterKeyWord__";

@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  selector: 'app-table',
  templateUrl: './table.component.html',
  styleUrl: './table.component.css'
})
export class TableComponent implements AfterViewInit {
  buttonActivated: boolean;
  displayedColumns: string[] = ['selected', 'place_name', 'postal_code', 'number_of_samples'];
  displayedSeqColumns: string[] = ['selected', 'postal_code', 'sequence_id', 'pang_lineage', 'date_sequenced'];
  dataSourcePLZ: MatTableDataSource<PLZElement>;
  dataSourceSeq: MatTableDataSource<SeqElement>;

  TableMode: Modes;
  enum = Modes;
  seqPLZAdditionFormControl: FormControl;
  dateStartFormControl: FormControl;
  dateEndFormControl: FormControl;
  
  PLZlist: any;

  isItDialouge: boolean;

  minDateInput: Date;
  maxDateInput: Date;
  currentPLZList: any;
  constructor(private BDSS: BaseDataServiceService, @Optional() public dialogRef: MatDialogRef<TableComponent>, private changeDetectorRef: ChangeDetectorRef) {
    this.isItDialouge = (dialogRef != null);

    this.dataSourcePLZ = new MatTableDataSource<PLZElement>();
    this.dataSourceSeq = new MatTableDataSource<SeqElement>();

    //overwriting filter trigger on datasourceSeq
    this.minDateInput = new Date(1970, 0, 1);
    this.maxDateInput = new Date(2100, 0, 1);


    //custom filtering function for dates
    this.dataSourceSeq.filterPredicate = (data: SeqElement, filter: string) => {
      var ret: boolean;

      var inputDate = new Date(data.date_sequenced)

      ret = (inputDate >= this.minDateInput && inputDate <= this.maxDateInput);
      if (filter != filterKeyword) {
        if (data.pang_lineage.toLowerCase().includes(filter)) {
          return ret && true;
        }
        if (data.postal_code.toLowerCase().includes(filter)) {
          return ret && true;
        }
        if (data.sequence_id.toLowerCase().includes(filter)) {
          return ret && true;
        }
        return false;
      }
      return ret;
    };

    this.TableMode = this.BDSS.getMode();
    this.PLZlist = this.BDSS.getPLZList();
    this.currentPLZList = this.BDSS.getSeqPLZList();

    this.buttonActivated = false;

    this.dateStartFormControl = new FormControl();
    this.dateEndFormControl = new FormControl();
    this.seqPLZAdditionFormControl = new FormControl("", [
      acceptedPLZValidator(this.PLZlist),
      forbiddenPLZValidator(this.currentPLZList),
      Validators.required
    ]);

  }

  closeDialouge() {
    this.dialogRef.close();
  }


  @ViewChild(MatSort) sort!: MatSort;
  @ViewChild(MatPaginator) paginator!: MatPaginator;

  ngAfterViewInit() {
    this.BDSS.getUpdateTableSubject().subscribe((result: any) => { this.updateTableEvent() });
    this.BDSS.getUpdateModeSubject().subscribe((result: any) => { this.updateTableEvent() })
  }

  togglePLZ(element: PLZElement) {

    var found = this.dataSourcePLZ.data.find((current) => current.postal_code == element.postal_code);

    if (typeof (found) != "undefined") {
      this.BDSS.setPLZFromTableInPLZMode(found.postal_code, !found.selected);
    }



  }

  toggleSeq(element: SeqElement) {
    var found = this.dataSourceSeq.data.find((current) => current.sequence_id == element.sequence_id);

    if (typeof (found) != "undefined") {
      this.BDSS.setSelectedSequence(found.sequence_id, !found.selected);
    }
  }


  updateTableEvent() {
    this.TableMode = this.BDSS.getMode();
    switch (this.TableMode) {

      case Modes.PostalCode:
        this.dataSourcePLZ.paginator = this.paginator;
        this.dataSourcePLZ.sort = this.sort;
        this.dataSourcePLZ.data = this.BDSS.getPLZDataSet();;

        break;

      case Modes.Sequence:
        this.dataSourceSeq.paginator = this.paginator;
        this.dataSourceSeq.sort = this.sort;
        this.dataSourceSeq.data = this.BDSS.getSeqDataSet();


        this.currentPLZList = this.BDSS.getSeqPLZList()

        this.seqPLZAdditionFormControl.setValidators([
          acceptedPLZValidator(this.PLZlist),
          forbiddenPLZValidator(this.currentPLZList),
          Validators.required
        ])
        this.seqPLZAdditionFormControl.updateValueAndValidity();
        break;

    }
    this.changeDetectorRef.detectChanges();
  }


  //--------------------------------PLZ Table---------
  applyFilterPLZTable(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSourcePLZ.filter = filterValue.trim().toLowerCase();
  }

  isAllSelectedPLZTable() {
    for (var i = 0, len = (this.dataSourcePLZ.data.length); len > i; i++) {
      if (this.dataSourcePLZ.data[i].selected == false) {
        return false;
      }
    }
    return true;
  }


  isNoneSelectedPLZTable() {
    for (var i = 0, len = (this.dataSourcePLZ.data.length); len > i; i++) {
      if (this.dataSourcePLZ.data[i].selected == true) {
        return false;
      }
    }
    return true;
  }

  masterTogglePLZTable() {
    this.BDSS.setAllPLZInPLZMode(!this.isAllSelectedPLZTable())
  }

  //---------------------Seq Table-------------
  //default dates are 01/01/1970 and 01/01/2100


  applyFilterSeqTable(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSourceSeq.filter = filterValue.trim().toLowerCase();
    this.dataSourceSeq._updateChangeSubscription();
  }

  applyStartDateFilterSeqTable(event: MatDatepickerInputEvent<Date>) {

    const filterValue = event.value;
    if (filterValue != null) {
      this.minDateInput = this.dateStartFormControl.value;
    }

    if (this.dataSourceSeq.filter == "") {
      this.dataSourceSeq.filter = filterKeyword;
    }

    this.dataSourceSeq._updateChangeSubscription();

  }

  applyEndDateFilterSeqTable(event: MatDatepickerInputEvent<Date>) {
    const filterValue = event.value;
    if (filterValue != null) {
      this.maxDateInput = this.dateEndFormControl.value;
    }

    if (this.dataSourceSeq.filter == "") {
      this.dataSourceSeq.filter = filterKeyword;
    }
    this.dataSourceSeq._updateChangeSubscription();

  }

  clearSeqTableDates(event: Event) {
    this.dateEndFormControl.setValue(null);
    this.dateStartFormControl.setValue(null);
    this.minDateInput.setTime(0);
    this.maxDateInput.setTime(4102448400000);

    if (this.dataSourceSeq.filter == filterKeyword) {
      this.dataSourceSeq.filter = "";
    }
    this.dataSourceSeq._updateChangeSubscription();
  }


  isAllSelectedSeqTable() {
    for (var i = 0, len = (this.dataSourceSeq.data.length); len > i; i++) {
      if (this.dataSourceSeq.data[i].selected == false) {
        return false;
      }
    }

    return true;
  }


  isNoneSelectedSeqTable() {
    for (var i = 0, len = (this.dataSourceSeq.data.length); len > i; i++) {
      if (this.dataSourceSeq.data[i].selected == true) {
        return false;
      }
    }

    return true;
  }

  masterToggleSeqTable() {
    this.BDSS.setAllPLZInSeqMode(!this.isAllSelectedSeqTable());
  }

  addSeqToTableFromForm() {
    this.buttonActivated = false;
    this.BDSS.addPLZFromTableinSeqMode(this.seqPLZAdditionFormControl.value).subscribe({
      next: (result: any) => this.buttonActivated = true,
      error: (error: any) => this.buttonActivated = true
    });
    //thumbs up emoji 👍
  }


  removePLZfromSeqMode(PLZ: any) {
    this.BDSS.removePLZinSeqModeFromTable(PLZ);
  }

}
