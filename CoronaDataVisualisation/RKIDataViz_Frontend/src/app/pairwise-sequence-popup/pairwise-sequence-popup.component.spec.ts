import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PairwiseSequencePopupComponent } from './pairwise-sequence-popup.component';

describe('PairwiseSequencePopupComponent', () => {
  let component: PairwiseSequencePopupComponent;
  let fixture: ComponentFixture<PairwiseSequencePopupComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [PairwiseSequencePopupComponent]
    })
      .compileComponents();

    fixture = TestBed.createComponent(PairwiseSequencePopupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
