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
  present_PLZ: number;

}

@Component({
  selector: 'app-pangolin-lineage-popup-sequence-based-graph',
  templateUrl: './pangolin-lineage-popup-sequence-based-graph.component.html',
  styleUrl: './pangolin-lineage-popup-sequence-based-graph.component.css'
})
export class PangolinLineagePopupSequenceBasedGraphComponent {

  dateStartFormControl: FormControl;
  dateEndFormControl: FormControl;

  minDateInput: Date;
  maxDateInput: Date;

  displayedColumns = ["selected", "pangolin lineage", "count", "present_PLZ"]

  minCount: number;

  tableData: any;

  minDate: Date;
  maxDate: Date;

  @ViewChild(MatSort) sort!: MatSort;
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  constructor(private BDSS: BaseDataServiceService, private CS: ComparisonServiceService, private http: HttpClient, public dialogRef: MatDialogRef<PangolinLineagePopupSequenceBasedGraphComponent>) {
    this.tableData = new MatTableDataSource<pangolinElement>()

    this.maxDate = new Date()
    this.minDate = new Date()

    this.minDateInput = new Date(0);
    this.maxDateInput = new Date(4102448400000);
    http.post(environment.GET_PLZ_OF_PANGOLINS_PATH,
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
    console.log("old value")
    console.log(this.minDateInput)
    const filterValue = event.value;
    if (filterValue != null) {
      this.minDateInput = this.dateStartFormControl.value;
    }

  }

  updateMaxDatePicker(event: MatDatepickerInputEvent<Date>) {
    console.log("old value")
    console.log(this.maxDateInput)
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

    this.CS.PLZScatterPlotByPangolin(this.getPangolinThatAreTrue(), this.minCount, this.dateStartFormControl.value, this.dateEndFormControl.value)

  }

}
