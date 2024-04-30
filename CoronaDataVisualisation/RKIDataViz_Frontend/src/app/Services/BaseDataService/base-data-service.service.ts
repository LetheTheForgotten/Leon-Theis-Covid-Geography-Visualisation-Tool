import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from './../../../environments/environment';
import { BehaviorSubject, Observable, Subscriber, flatMap, map, mergeMap } from 'rxjs'
import { existInLocalStorage, persistentData } from '../../persistent-data/persistent-data';
import { persistentMap } from '../../persistent-data/persistent-map';
import { persistentObject } from '../../persistent-data/persistent-object';


export interface PLZElement {
  postal_code: string;
  selected: boolean;
  number_of_samples: number;
  place_name: string;

}

export interface SeqElement {
  selected: boolean;
  postal_code: string;
  sequence_id: string;
  pang_lineage: string;
  date_sequenced: Date;
}

export enum Modes {
  Global,
  Sequence,
  PostalCode
}




@Injectable({
  providedIn: 'root'
})

export class BaseDataServiceService {


  //----------state variables------------///
  private Mode: persistentData<Modes>;

  //---------behvaourSubjects------------/
  private updateMapSubject: BehaviorSubject<Boolean>;

  private updateTableSubject: BehaviorSubject<Boolean>;

  private updateModeSubject: BehaviorSubject<Boolean>;

  //------------PLZ mode variables------------//
  private PLZDataSet: persistentData<Array<PLZElement>>;


  //------------Sequence Mode Variables-------///
  private SeqDataSet: persistentObject<Array<SeqElement>>;

  private activePLZList: persistentMap<string, boolean>;

  private plzList: Array<string>;

  private activePLZListInSeqModeOverwrite: boolean;
  private PLZDatasetOverwrite: boolean;

  //-------------Popout Window Variables----------///
  private MSAState: boolean = true;
  private sequenceAlignState: boolean = true;

  constructor(private http: HttpClient) {

    this.Mode = new persistentData<Modes>(Modes.PostalCode, "BDSS.data.Mode", (value: any) => this.updateModeSubject.next(false));


    this.SeqDataSet = new persistentObject<Array<SeqElement>>(new Array<SeqElement>, "BDSS.data.SeqDataSet", (value: any) => {
      this.updateTableSubject.next(false);

    },http);
    if (existInLocalStorage("BDSS.data.activePLZList")) {
      this.activePLZListInSeqModeOverwrite = false;
    }
    else {
      this.activePLZListInSeqModeOverwrite = true;
    }
    this.activePLZList = new persistentMap<string, boolean>(new Map<string, boolean>(), "BDSS.data.activePLZList", (value: any) => {
      this.updateTableSubject.next(false);
      this.updateMapSubject.next(false);
    });

    this.plzList = new Array<string>;

    this.updateTableSubject = new BehaviorSubject<Boolean>(true);
    this.updateMapSubject = new BehaviorSubject<Boolean>(true);
    this.updateModeSubject = new BehaviorSubject<Boolean>(true);

    if (existInLocalStorage("BDSS.data.PLZDataSet")) {
      this.PLZDatasetOverwrite = false;
    }
    else {
      this.PLZDatasetOverwrite = true;
    }
    this.PLZDataSet = new persistentData<Array<PLZElement>>(new Array<PLZElement>, "BDSS.data.PLZDataSet", (value: any) => {
      this.updateTableSubject.next(false);
      this.updateMapSubject.next(false);
    });

    //initializes PLZ and sequence data (via PLZlist)
    this.getPLZ().subscribe({
      next: (result: any) => {

        if (this.PLZDatasetOverwrite) {
          this.PLZDataSet.set(result);
        }


        var tmpMap = new Map<string, boolean>()

        //setting selected Seq PLZs
        for (var i = 0, len = (this.PLZDataSet.get().length); len > i; i++) {
          tmpMap.set(this.PLZDataSet.get()[i].postal_code, false);
          this.plzList.push(this.PLZDataSet.get()[i].postal_code);
        }
        if (this.activePLZListInSeqModeOverwrite) {
          this.activePLZList.set(tmpMap);
        }
        this.updateTableSubject.next(false);

      }, error: (error: any) => console.error(error)
    });

  }

  signalMapUpdate() {
    this.updateMapSubject.next(false);
  }

  signalTableUpdate() {
    this.updateTableSubject.next(false);
  }

  signalModeUpdate() {
    this.updateModeSubject.next(false);
  }

  //getters and setters-------------------------------------------
  getMSAState() {
    return this.MSAState;
  }

  setMSAState(state: boolean) {
    this.MSAState = state;
  }

  getSeqAlignState() {
    return this.sequenceAlignState;
  }

  setSeqAlignState(state: boolean) {
    this.sequenceAlignState = state;
  }
  //returns PLZ that are selected in PLZ mode
  getPLZDataSetSelected() {
    return this.PLZDataSet.get().filter((element: any) => element.selected);
  }

  getSeqDataSetSelected() {
    return this.SeqDataSet.get().filter((element: any) => element.selected);
  }

  getPLZList() {
    return this.plzList;
  }

  //gets geoJSON file for initial visualization of map
  getGeoJSON(): any {
    return this.http.get(environment.GET_GEO_JSON_PATH);
  }

  getMode() {
    return this.Mode.get();
  }

  setMode(mode: Modes) {
    this.Mode.set(mode);
    this.updateModeSubject.next(false);
  }

  getUpdateMapSubject() {
    return this.updateMapSubject;
  }

  getUpdateTableSubject() {
    return this.updateTableSubject;
  }

  getUpdateModeSubject() {
    return this.updateModeSubject;
  }

  getPLZDataSet() {
    return this.PLZDataSet.get();
  }

  getSeqDataSet() {
    return this.SeqDataSet.get();
  }

  getSeqPLZList() {
    return this.activePLZList.get();
  }

  //return list of PLZ
  getPLZ() {
    return this.http.get(environment.GET_PLZ_LIST_PATH);
  }

  //Seq mode functions-------------------------------------------------



  addPLZFromMapinSeqMode(PLZ: string) {

    //redundancy check
    if (this.activePLZList.get().get(PLZ)) {
      return new Observable((sub: any) => sub.next(false));
    }

    return this.http.get(environment.GET_SEQ_TABLE_FROM_PLZ_PATH + PLZ).pipe(
      map((result: any) => {
        //asynchronous data is fun
        var tmpActivePLZ = this.activePLZList.get();
        if (tmpActivePLZ.get(PLZ)) {
          return false;
        }

        var tmpSeqData = this.SeqDataSet.get();
        result.splice(result.length, 0, ...tmpSeqData)
        this.SeqDataSet.set(result);

        this.activePLZList.set(tmpActivePLZ.set(PLZ, true));
        this.updateTableSubject.next(false);

        return true;

      }
      )
    );
  }

  addPLZFromTableinSeqMode(PLZ: string) {
    //redundancy check
    if (this.activePLZList.get().get(PLZ)) {
      return new Observable((sub: any) => sub.next(false));
    }

    return this.http.get<Array<SeqElement>>(environment.GET_SEQ_TABLE_FROM_PLZ_PATH + PLZ).pipe(
      map((result: Array<SeqElement>) => {
        for (var i = 0; result.length > i; i++) {
          result[i].date_sequenced = new Date(result[i].date_sequenced);
        }

        //asynchronous data is fun
        var tmpActivePLZ = this.activePLZList.get()
        if (tmpActivePLZ.get(PLZ)) {
          return false;
        }
        var tmpSeqData = this.SeqDataSet.get()
        result.splice(result.length, 0, ...tmpSeqData)
        this.SeqDataSet.set(result);

        this.activePLZList.set(tmpActivePLZ.set(PLZ, true));

        this.updateTableSubject.next(false);
        this.updateMapSubject.next(false);

        return true;

      }
      )
    );
  }

  removePLZinSeqModeFromMap(PLZ: string) {
    var tmpActivePLZ = this.activePLZList.get();

    if (tmpActivePLZ.get(PLZ)) {
      this.activePLZList.set(tmpActivePLZ.set(PLZ, false));

      var tmpSeqData = this.SeqDataSet.get();
      for (var i = 0; tmpSeqData.length > i;) {
        if (tmpSeqData[i].postal_code == PLZ) {
          tmpSeqData.splice(i, 1);
        }
        else {
          i++;
        }
      }
      this.SeqDataSet.update();
      this.updateTableSubject.next(false);

    }

  }

  removePLZinSeqModeFromTable(PLZ: string) {
    var tmpPLZ = this.activePLZList.get()
    if (tmpPLZ.get(PLZ)) {
      this.activePLZList.set(tmpPLZ.set(PLZ, false));

      var tmpSeqData = this.SeqDataSet.get()
      for (var i = 0; tmpSeqData.length > i;) {
        if (tmpSeqData[i].postal_code == PLZ) {
          tmpSeqData.splice(i, 1);
        }
        else {
          i++;
        }
      }
      this.SeqDataSet.update();

      this.updateMapSubject.next(false);
      this.updateTableSubject.next(false);
    }

  }

  setSelectedSequence(sequenceID: string, value: boolean) {
    var found = this.SeqDataSet.get().find((current) => current.sequence_id == sequenceID);
    if (typeof (found) != "undefined") {
      found.selected = value;
      this.SeqDataSet.update();
    }
  }

  setPLZFromTableInSeqMode(PLZ: string): any {
    this.http.get(environment.GET_SEQ_TABLE_FROM_PLZ_PATH + PLZ).subscribe((result: any) => {
      this.SeqDataSet.set(result);
      this.updateMapSubject.next(false);
    });
  }

  setAllPLZInSeqMode(value: boolean) {
    var tmpDataSourceSeq = this.SeqDataSet.get();
    for (var i = 0, len = (tmpDataSourceSeq.length); len > i; i++) {
      tmpDataSourceSeq[i].selected = value;
    }
    this.SeqDataSet.update();
    this.updateMapSubject.next(false);
  }

  setPLZFromMapInSeqMode(PLZ: string, Selected: boolean): any {
    if (Selected) {
      this.addPLZFromMapinSeqMode(PLZ);
    }
    else {
      this.removePLZinSeqModeFromMap(PLZ);
    }

  }



  //PLZ mode functions----------------------------------------------------------



  setPLZInPLZMode(plz: string, value: boolean) {
    var found = this.PLZDataSet.get().find((current) => current.postal_code == plz);
    if (typeof (found) != "undefined") {
      found.selected = value;
      this.PLZDataSet.update();
    }

  }
  setAllPLZInPLZMode(value: boolean) {
    var tmpDataSourcePLZ = this.PLZDataSet.get()
    for (var i = 0, len = (tmpDataSourcePLZ.length); len > i; i++) {
      tmpDataSourcePLZ[i].selected = value;
    }
    this.PLZDataSet.update();
    this.updateMapSubject.next(false);
  }


  setPLZFromTableInPLZMode(plz: string, value: boolean) {
    this.setPLZInPLZMode(plz, value);
    this.updateMapSubject.next(false);
  }

  setPLZfromMapInPLZMode(plz: string, value: boolean) {
    this.setPLZInPLZMode(plz, value);
    this.updateTableSubject.next(false);
  }

}
