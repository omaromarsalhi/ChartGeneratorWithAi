import { Component, OnInit } from '@angular/core';
import { ChartType } from '../../chart/apex/apex.model';

import {
  linewithDataChart
} from './data';

@Component({
  selector: 'app-generated-chart',
  templateUrl: './generated-chart.component.html',
  styleUrls: ['./generated-chart.component.scss']
})
export class GeneratedChartComponent implements OnInit {
  // bread crumb items
  breadCrumbItems: Array<{}>;
  
  linewithDataChart: ChartType;

  
  constructor() { }

  ngOnInit() {
    this.breadCrumbItems = [{ label: 'Charts' }, { label: 'Apex charts', active: true }];

    /**
     * Fethches the chart data
     */
    this._fetchData();
  }

  /**
   * Fetches the chart data
   */
  private _fetchData() {
    this.linewithDataChart = linewithDataChart;
  }



}
