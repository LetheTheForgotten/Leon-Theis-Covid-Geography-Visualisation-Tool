import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';

import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { MaterialModule } from './MaterialModuleScript';
import { MapElementComponent } from './Elements/map-element/map-element.component';


import { TableComponent } from './Elements/table/table.component';
import { GraphviewComponent } from './Elements/graphview/graphview.component'
import { RouterOutlet, provideRouter } from '@angular/router';
import { routes } from './app-routing.module';
import { MainPageComponent } from './main-page/main-page.component';
import { PangolinLineagePopupComponent } from './pangolin-lineage-popup/pangolin-lineage-popup.component';
import { PangolinLineagePopupSequenceBasedGraphComponent } from './pangolin-lineage-popup-sequence-based-graph/pangolin-lineage-popup-sequence-based-graph.component';
import { SummaryPopupComponent } from './summary-popup/summary-popup.component';
import { MSAPopupComponent } from './msa-popup/msa-popup.component';
import { PairwiseSequencePopupComponent } from './pairwise-sequence-popup/pairwise-sequence-popup.component';


@NgModule({
  declarations: [
    AppComponent,
    MapElementComponent,
    TableComponent,
    GraphviewComponent,
    MainPageComponent,
    PangolinLineagePopupComponent,
    PangolinLineagePopupSequenceBasedGraphComponent,
    SummaryPopupComponent,
    MSAPopupComponent,
    PairwiseSequencePopupComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    NoopAnimationsModule,
    MaterialModule,
    RouterOutlet
  ],
  providers: [provideRouter(routes)],
  bootstrap: [AppComponent]
})
export class AppModule { }
