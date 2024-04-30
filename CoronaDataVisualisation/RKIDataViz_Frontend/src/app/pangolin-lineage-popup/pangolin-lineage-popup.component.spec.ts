import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PangolinLineagePopupComponent } from './pangolin-lineage-popup.component';

describe('PangolinLineagePopupComponent', () => {
  let component: PangolinLineagePopupComponent;
  let fixture: ComponentFixture<PangolinLineagePopupComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [PangolinLineagePopupComponent]
    })
      .compileComponents();

    fixture = TestBed.createComponent(PangolinLineagePopupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
