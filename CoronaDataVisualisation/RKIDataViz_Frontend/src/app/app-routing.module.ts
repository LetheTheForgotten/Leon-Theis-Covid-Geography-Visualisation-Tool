import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TableComponent } from './Elements/table/table.component';
import { GraphviewComponent } from './Elements/graphview/graphview.component';
import { MainPageComponent } from './main-page/main-page.component';

export const routes: Routes = [{ path: "", component: MainPageComponent }, { path: "table", component: TableComponent }, { path: "graph", component: GraphviewComponent }];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
