import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GeneratedChartComponent } from './generated-chart.component';

describe('GeneratedChartComponent', () => {
  let component: GeneratedChartComponent;
  let fixture: ComponentFixture<GeneratedChartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GeneratedChartComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GeneratedChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
