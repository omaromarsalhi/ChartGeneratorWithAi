
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { NgApexchartsModule } from 'ng-apexcharts';
import { ChartsModule } from 'ng2-charts';
import { NgxChartistModule } from 'ngx-chartist';
import { NgxEchartsModule } from 'ngx-echarts';

import { UIModule } from '../../shared/ui/ui.module';
import { ChartAIRoutingModule } from './chartAi-routing.module';
import { GeneratedChartComponent } from './generated-chart/generated-chart.component';


@NgModule({
  declarations: [GeneratedChartComponent],
  imports: [
    CommonModule,
    ChartAIRoutingModule,
    UIModule,
    NgApexchartsModule,
    ChartsModule,
    NgxChartistModule,
    NgxEchartsModule.forRoot({
      echarts: () => import('echarts')
    })
  ]
})
export class ChartAIModule { }
