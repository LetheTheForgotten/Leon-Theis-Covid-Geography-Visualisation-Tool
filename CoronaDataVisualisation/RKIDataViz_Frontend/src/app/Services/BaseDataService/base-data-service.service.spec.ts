import { TestBed } from '@angular/core/testing';

import { BaseDataServiceService } from './base-data-service.service';

describe('BaseDataServiceService', () => {
  let service: BaseDataServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BaseDataServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
