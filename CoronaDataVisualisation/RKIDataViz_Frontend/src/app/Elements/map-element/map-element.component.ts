import { Component, AfterViewInit } from '@angular/core';
import * as L from 'leaflet';
import { BaseDataServiceService, Modes } from '../../Services/BaseDataService/base-data-service.service';
import { GeoJsonObject } from 'geojson';


@Component({
  selector: 'app-map-element',
  templateUrl: './map-element.component.html',
  styleUrl: './map-element.component.css'
})


export class MapElementComponent implements AfterViewInit {
  private map: L.Map | undefined;

  geoLayerPLZMode: any;
  geoLayerSeqMode: any;
  MapMode: Modes;
  enum = Modes;

  ClickState: boolean;

  infoPanel: any;
  _div: any;

  PLZtoLayerIdMapPLZMode: Map<string, string>;
  PLZtoLayerIdMapSeqMode: Map<string, string>;
  constructor(private BDSS: BaseDataServiceService) {
    this.MapMode = this.BDSS.getMode();
    this.ClickState = true;

    //---------------hashmap to store id values of PLZ---------
    this.PLZtoLayerIdMapPLZMode = new Map<string, string>;
    this.PLZtoLayerIdMapSeqMode = new Map<string, string>;
  }

  updateModeEvent() {
    switch (this.BDSS.getMode()) {

      case Modes.Global:
        console.log("Map updated to Global");
        this.MapMode = Modes.Global;

        break;

      case Modes.PostalCode:

        if (this.map?.hasLayer(this.geoLayerSeqMode)) {
          this.map?.removeLayer(this.geoLayerSeqMode);
        }

        if (!this.map?.hasLayer(this.geoLayerPLZMode)) {
          this.map?.addLayer(this.geoLayerPLZMode);
        }

        this.MapMode = Modes.PostalCode;

        break;

      case Modes.Sequence:

        if (this.map?.hasLayer(this.geoLayerPLZMode)) {
          this.map?.removeLayer(this.geoLayerPLZMode);
        }

        if (!this.map?.hasLayer(this.geoLayerSeqMode)) {
          this.map?.addLayer(this.geoLayerSeqMode);
        }

        this.MapMode = Modes.Sequence;
    }
  }

  //throw out through iterating over layergroups rather than checking last state
  updateMapEvent() {

    switch (this.MapMode) {

      case Modes.Global:
        break;

      case Modes.PostalCode:

        var dataSet: any;
        dataSet = this.BDSS.getPLZDataSet();

        //iterates through each element and updates styling
        for (var i = 0, len = (dataSet.length); len > i; i++) {
          var element = dataSet[i];

          if (this.PLZtoLayerIdMapPLZMode.has(element.postal_code)) {
            var tempGeoLayer = this.geoLayerPLZMode.getLayer(this.PLZtoLayerIdMapPLZMode.get(element.postal_code));

            //code for flyover
            if (element.selected == true && tempGeoLayer.feature.properties.selected == false) {
              try {
                //for some inexplicable reason the coordinates within feature.geometry are long,lat not lat,long
                var lon = tempGeoLayer.feature.properties.Coordinates
                this.map?.flyTo(tempGeoLayer.feature.properties.Coordinates, 10)
              }
              catch (e) {
                console.log(e)

              }
            }

            tempGeoLayer.feature.properties.selected = element.selected;


            this.geoLayerPLZMode.resetStyle(tempGeoLayer);
          }
          else {
            console.log("PLZ does not exist or is not in geodata: ");
            console.log(element.postal_code);
          }
        }
        break;

      case Modes.Sequence:
        var dataSet: any;
        dataSet = this.BDSS.getSeqPLZList();

        //iterates through each element and updates styling
        for (let [PLZ, Selected] of dataSet) {
          if (this.PLZtoLayerIdMapSeqMode.has(PLZ)) {

            var tempGeoLayer = this.geoLayerSeqMode.getLayer(this.PLZtoLayerIdMapSeqMode.get(PLZ));

            tempGeoLayer.feature.properties.selected = Selected;
            this.geoLayerSeqMode.resetStyle(tempGeoLayer);
          }
          else {
            console.log("PLZ does not exist or is not in geodata: ");
            console.log(PLZ);
          }
        }
        break;

    }

  }

  //---------outside setters and getters----

  setSelectedStatusOfPLZ(status: boolean, PLZ: string) {
    var feature = this.geoLayerPLZMode.getLayer(this.PLZtoLayerIdMapPLZMode.get(PLZ))
    feature.properties.selected = status;
  }

  //-----GeoJson functions-----------
  style(feature: any) {
    //if true, green 
    if (feature.properties.selected) {
      return {
        fillColor: '#008000',
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
      };
    }
    //else red
    return {
      fillColor: '#800026',
      weight: 2,
      opacity: 1,
      color: 'white',
      dashArray: '3',
      fillOpacity: 0.7
    };
  }

  //----------PLZ Mode Listeners---------------
  highlightSelected(e: any) {
    var layer = e.target;

    layer.setStyle({
      weight: 5,
      color: '#666',
      dashArray: '',
      fillOpacity: 0.7
    });
    this.infoPanel.update(layer.feature.properties);
    layer.bringToFront();
  }

  removeHighlight(e: any) {
    e.target.setStyle(this.style(e.target.feature))
    this.infoPanel.update();
  }

  onClick(e: any) {
    if (this.ClickState) {
      this.ClickState = false;
      //colour change is triggered through resetStyle, triggered through removeHiglight
      e.target.feature.properties.selected = !e.target.feature.properties.selected;
      this.BDSS.setPLZfromMapInPLZMode(e.target.feature.properties.plz, e.target.feature.properties.selected);

    }
    this.ClickState = true;
  }

  //adds listeners to each element of the layer
  //also stores id - PLZ key value pair in map
  onEachFeature(feature: any, layer: any) {

    layer.on({
      mouseover: (event: any) => this.highlightSelected(event),
      mouseout: (event: any) => this.removeHighlight(event),
      click: (event: any) => this.onClick(event)
    })

  }

  //----------Sequence Mode Listeners---------------
  highlightSelectedSeqMode(e: any) {
    var layer = e.target;

    layer.setStyle({
      weight: 5,
      color: '#666',
      dashArray: '',
      fillOpacity: 0.7
    });
    this.infoPanel.update(layer.feature.properties);
    layer.bringToFront();
  }

  removeHighlightSeqMode(e: any) {
    e.target.setStyle(this.style(e.target.feature))
    this.infoPanel.update();
  }

  onClickSeqMode(e: any) {
    if (this.ClickState) {
      this.ClickState = false;

      //subscriptions to deal with asynchronous data
      if (e.target.feature.properties.selected) {
        e.target.feature.properties.selected = false;
        this.BDSS.removePLZinSeqModeFromMap(e.target.feature.properties.plz);
        this.ClickState = true;
      }
      else {
        e.target.feature.properties.selected = true;
        this.BDSS.addPLZFromMapinSeqMode(e.target.feature.properties.plz).subscribe(
          {
            next: (result: any) => this.ClickState = true,
            error: (error: any) => this.ClickState = true
          });

      }
      this.BDSS.setPLZFromMapInSeqMode(e.target.feature.properties.plz, e.target.feature.properties.selected);
    }
    else {
      console.log("click event denied")
    }
  }

  //adds listeners to each element of the layer
  onEachFeatureSeqMode(feature: any, layer: any) {

    layer.on({
      mouseover: (event: any) => this.highlightSelectedSeqMode(event),
      mouseout: (event: any) => this.removeHighlightSeqMode(event),
      click: (event: any) => this.onClickSeqMode(event)
    })

  }



  //--------------------------------------------------------

  private initMap(param: any): void {
    this.map = L.map('map', {
      maxBounds: new L.LatLngBounds(L.latLng(55.845876280576384, 1.786342618148489), L.latLng(47.27346006356369, 15.409389288587835)),
      center: [51.1890020829787, 6.794448762571533],
      zoom: 5

    });



    const tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {

      maxZoom: 18,
      minZoom: 5,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    });

    tiles.addTo(this.map);



    this.geoLayerPLZMode = L.geoJSON(param, { style: this.style, onEachFeature: (feature: any, layer: any) => this.onEachFeature(feature, layer) }).addTo(this.map);
    //need to copy else both use the same pointer
    this.geoLayerSeqMode = L.geoJSON(JSON.parse(JSON.stringify(param)), { style: this.style, onEachFeature: (feature: any, layer: any) => this.onEachFeatureSeqMode(feature, layer) });
    //this.geoLayer.setOpacity(0)

    console.log("this is to provide a breakpoint");

    this.geoLayerPLZMode.eachLayer((layer: any) => this.PLZtoLayerIdMapPLZMode.set(layer.feature.properties.plz, layer._leaflet_id));
    this.geoLayerSeqMode.eachLayer((layer: any) => this.PLZtoLayerIdMapSeqMode.set(layer.feature.properties.plz, layer._leaflet_id));

    //----setup info-panel----//
    this.infoPanel = new L.Control()

    this.infoPanel.onAdd = (map: any) => {
      this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"

      this.infoPanel.update();
      return this._div;
    };

    //override update function of info-panel to determine info shown
    // method that we will use to update the control based on feature properties passed

    this.infoPanel.update = (props: any) => {
      this._div.innerHTML = '<h4>Info Box</h4>' + (props ?
        '<b>' + props.note + '</b><br />' + props.total_samples + ' Available Samples:'
        : 'Select a PLZ');

    };


    this.infoPanel.addTo(this.map)

    this.BDSS.getUpdateMapSubject().subscribe((result: any) => { this.updateMapEvent() });
    this.BDSS.getUpdateModeSubject().subscribe((result: any) => { this.updateModeEvent() });

  }



  ngAfterViewInit(): void {
    //initialize data
    this.BDSS.getGeoJSON().subscribe((result: GeoJsonObject) => { this.initMap(result); }, (error: any) => console.error(error));

  }
}
