import { Component, ViewChild } from '@angular/core';
import { BaseDataServiceService } from '../Services/BaseDataService/base-data-service.service';
import { ComparisonServiceService } from '../Services/ComparisonService/comparison-service.service';
import { HttpClient } from '@angular/common/http';
import { MatDialogRef } from '@angular/material/dialog';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';
import { FormControl } from '@angular/forms';
import { MatDatepickerInputEvent } from '@angular/material/datepicker';
import { environment } from '../../environments/environment';
import { MatPaginator } from '@angular/material/paginator';
interface pangolinElement {
  selected: boolean;
  count: number;
  lineage: string;
  maxOrMin: Date;

}

@Component({
  selector: 'app-pangolin-lineage-popup',
  templateUrl: './pangolin-lineage-popup.component.html',
  styleUrl: './pangolin-lineage-popup.component.css'
})
export class PangolinLineagePopupComponent {

  dateStartFormControl: FormControl;
  dateEndFormControl: FormControl;

  minDateInput: Date;
  maxDateInput: Date;

  displayedColumns = ["selected", "pangolin lineage", "count"]

  minCount: number;

  tableData: any;

  minDate: Date;
  maxDate: Date;

  @ViewChild(MatSort) sort!: MatSort;
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  constructor(private BDSS: BaseDataServiceService, private CS: ComparisonServiceService, private http: HttpClient, public dialogRef: MatDialogRef<PangolinLineagePopupComponent>) {
    this.tableData = new MatTableDataSource<pangolinElement>()

    this.maxDate = new Date()
    this.minDate = new Date()

    this.minDateInput = new Date(0);
    this.maxDateInput = new Date(4102448400000);

    http.post(environment.GET_PANGOLINS_OF_PLZ_PATH,
      this.BDSS.getPLZDataSetSelected()).subscribe({
        next: (result: any) => {
          this.tableData.data = result;
          this.minDate = new Date(this.tableData.data[0].maxOrMin);
          this.maxDate = new Date(this.tableData.data[1].maxOrMin);
          this.minDateInput = new Date(this.minDate)
          this.maxDateInput = new Date(this.maxDate)
        }, error: (error: any) => console.log(error)
      })
    this.minCount = 0

    this.dateStartFormControl = new FormControl();
    this.dateEndFormControl = new FormControl();
  }

  clearDates() {
    this.dateEndFormControl.setValue(null);
    this.dateStartFormControl.setValue(null);

    this.minDateInput = new Date(this.minDate);
    this.maxDateInput = new Date(this.maxDate);
  }

  updateMinDatePicker(event: MatDatepickerInputEvent<Date>) {
    const filterValue = event.value;
    if (filterValue != null) {
      this.minDateInput = this.dateStartFormControl.value;
    }

  }

  updateMaxDatePicker(event: MatDatepickerInputEvent<Date>) {
    const filterValue = event.value;

    if (filterValue != null) {
      this.maxDateInput = this.dateStartFormControl.value;
    }
  }

  ngAfterViewInit() {
    this.tableData.sort = this.sort;
    this.tableData.paginator = this.paginator;
    this.minDateInput = new Date(this.minDate);
    this.maxDateInput = new Date(this.maxDate);
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.tableData.filter = filterValue.trim().toLowerCase();
  }

  toggleDialouge(element: pangolinElement) {
    var found = this.tableData.data.filter((current: any) => current.lineage == element.lineage)[0];
    found.selected = !found.selected;
  }

  getPangolinThatAreTrue() {
    return this.tableData.data.filter((current: any) => current.selected == true)
  }

  isAllSelectedDialouge() {
    for (var i = 0, len = (this.tableData.data.length); len > i; i++) {
      if (this.tableData.data[i].selected == false) {
        return false;
      }
    }

    return true;

  }

  isNoneSelectedDialouge() {
    for (var i = 0, len = (this.tableData.data.length); len > i; i++) {
      if (this.tableData.data[i].selected == true) {
        return false;
      }
    }

    return true;
  }

  masterToggleDialouge() {
    if (this.isAllSelectedDialouge()) {
      for (var i = 0, len = (this.tableData.data.length); len > i; i++) {
        this.tableData.data[i].selected = false;
      }
    }
    else {
      for (var i = 0, len = (this.tableData.data.length); len > i; i++) {
        this.tableData.data[i].selected = true;
      }
    }
  }

  closeDialouge() {
    this.dialogRef.close()
  }


  submitPLZChart() {
    if (this.minCount == null || typeof (this.minCount) == "undefined") {
      this.minCount = 0
    }

    this.CS.PLZScatterPlotByPLZ(this.getPangolinThatAreTrue(), this.minCount, this.dateStartFormControl.value, this.dateEndFormControl.value)

  }

  submitAllPLZChart() {
    this.masterToggleDialouge()
    this.CS.PLZScatterPlotByPLZ(this.getPangolinThatAreTrue(), 0, this.minDate, this.maxDate)
  }

}
