import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PangolinLineagePopupSequenceBasedGraphComponent } from './pangolin-lineage-popup-sequence-based-graph.component';

describe('PangolinLineagePopupSequenceBasedGraphComponent', () => {
  let component: PangolinLineagePopupSequenceBasedGraphComponent;
  let fixture: ComponentFixture<PangolinLineagePopupSequenceBasedGraphComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [PangolinLineagePopupSequenceBasedGraphComponent]
    })
      .compileComponents();

    fixture = TestBed.createComponent(PangolinLineagePopupSequenceBasedGraphComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
