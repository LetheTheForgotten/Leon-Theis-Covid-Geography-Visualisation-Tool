import { TestBed } from '@angular/core/testing';

import { ComparisonServiceService } from './comparison-service.service';

describe('ComparisonServiceService', () => {
  let service: ComparisonServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ComparisonServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
