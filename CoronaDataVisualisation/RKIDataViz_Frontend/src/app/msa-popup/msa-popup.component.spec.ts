import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MSAPopupComponent } from './msa-popup.component';

describe('MSAPopupComponent', () => {
  let component: MSAPopupComponent;
  let fixture: ComponentFixture<MSAPopupComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [MSAPopupComponent]
    })
      .compileComponents();

    fixture = TestBed.createComponent(MSAPopupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
