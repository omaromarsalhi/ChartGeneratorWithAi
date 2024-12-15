import { MenuItem } from './menu.model';

export const MENU: MenuItem[] = [
    {
        id: 1,
        icon: 'bxs-bar-chart-alt-2',
        label: 'MENUITEMS.CHARTS.TEXT',
        subItems: [
            {
                id: 2,
                label: 'MENUITEMS.CHARTS.LIST.APEX',
                link: '/charts/apex',
                parentId: 1
            },
            {
                id: 3,
                label: 'MENUITEMS.CHARTS.LIST.CHARTJS',
                link: '/charts/chartjs',
                parentId: 1
            },
            {
                id: 4,
                label: 'MENUITEMS.CHARTS.LIST.CHARTIST',
                link: '/charts/chartist',
                parentId: 1
            },
            {
                id: 5,
                label: 'MENUITEMS.CHARTS.LIST.ECHART',
                link: '/charts/echart',
                parentId: 1
            }
        ]
    },
    {
        id: 6,
        icon: 'bxs-bar-chart-alt-2',
        label: 'MENUITEMS.CHARTS.TEXT',
        subItems: [
            {
                id: 7,
                label: 'AI.Chart',
                link: '/ai_charts/ai_generator',
                parentId: 6
            }
        ]
    },
];

