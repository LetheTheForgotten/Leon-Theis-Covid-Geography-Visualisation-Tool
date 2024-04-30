import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MapElementComponent } from './map-element.component';

describe('MapElementComponent', () => {
  let component: MapElementComponent;
  let fixture: ComponentFixture<MapElementComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [MapElementComponent]
    })
      .compileComponents();

    fixture = TestBed.createComponent(MapElementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
