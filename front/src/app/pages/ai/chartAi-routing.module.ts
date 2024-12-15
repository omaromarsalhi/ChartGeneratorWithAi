import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { GeneratedChartComponent } from './generated-chart/generated-chart.component';

const routes: Routes = [
    {
        path: 'ai_generator',
        component: GeneratedChartComponent
    },
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})

export class ChartAIRoutingModule { }
