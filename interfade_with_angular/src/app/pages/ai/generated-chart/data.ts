import { ChartType } from '../../chart/apex/apex.model';



// const dashedLineChart: ChartType = {
//     chart: {
//         height: 380,
//         type: 'line',
//         zoom: {
//             enabled: true
//         },
//         toolbar: {
//             show: true,
//         }
//     },
//     colors: ['#556ee6', '#f46a6a', '#34c38f'],
//     dataLabels: {
//         enabled: false
//     },
//     stroke: {
//         width: [3, 4, 3],
//         curve: 'straight',
//         dashArray: [0, 8, 5]
//     },
//     series: [{
//         name: 'Session Duration',
//         data: [45, 52, 38, 24, 33, 26, 21, 20, 6, 8, 15, 10]
//     },
//     {
//         name: 'Page Views',
//         data: [36, 42, 60, 42, 13, 18, 29, 37, 36, 51, 32, 35]
//     },
//     {
//         name: 'Total Visits',
//         data: [89, 56, 74, 98, 72, 38, 64, 46, 84, 58, 46, 49]
//     }
//     ],
//     title: {
//         text: 'Page Statistics',
//         align: 'left'
//     },
//     markers: {
//         size: 1,

//         hover: {
//             sizeOffset: 6
//         }
//     },
//     xaxis: {
//         categories: ['01 Jan', '02 Jan', '03 Jan', '04 Jan', '05 Jan', '06 Jan', '07 Jan', '08 Jan', '09 Jan',
//             '10 Jan', '11 Jan', '12 Jan'
//         ],
//     },
//     tooltip: {
//         y: [{
//             title: {
//                 formatter: (val) => {
//                     return val + ' (mins)';
//                 }
//             }
//         }, {
//             title: {
//                 formatter: (val) => {
//                     return val + ' per session';
//                 }
//             }
//         }, {
//             title: {
//                 formatter: (val) => {
//                     return val;
//                 }
//             }
//         }]
//     },
//     grid: {
//         borderColor: '#f1f1f1',
//     }
// };


const linewithDataChart: ChartType = {
    chart: {
      height: 380,
      type: "line",
      zoom: {
        enabled: false
      },
      toolbar: {
        show: false
      }
    },
    colors: [
      "#556ee6",
      "#34c38f"
    ],
    dataLabels: {
      enabled: true
    },
    stroke: {
      width: [
        3,
        3
      ],
      curve: "straight"
    },
    series: [
      {
        name: "High - 2018",
        data: [
          26,
          24,
          32,
          36,
          33,
          31,
          33
        ]
      },
      {
        name: "Low - 2018",
        data: [
          14,
          11,
          16,
          12,
          17,
          13,
          12
        ]
      }
    ],
    title: {
      text: "Average High & Low Temperature",
      align: "left"
    },
    grid: {
      row: {
        colors: [
          "transparent",
          "transparent"
        ],
        opacity: 0.2
      },
      borderColor: "#f1f1f1"
    },
    markers: {
      style: "inverted",
      size: 6
    },
    xaxis: {
      categories: [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul"
      ],
      title: {
        text: "Month"
      }
    },
    yaxis: {
      title: {
        text: "Temperature"
      },
      min: 5,
      max: 40
    },
    legend: {
      position: "top",
      horizontalAlign: "right",
      floating: true,
      offsetY: -25,
      offsetX: -5
    },
    responsive: [
      {
        breakpoint: 600,
        options: {
          chart: {
            toolbar: {
              show: false
            }
          },
          legend: {
            show: false
          }
        }
      }
    ]
  };


export {
    linewithDataChart
};
