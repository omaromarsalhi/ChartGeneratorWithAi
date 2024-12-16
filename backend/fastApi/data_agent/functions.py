from llama_index.core.workflow import Context
from fastApi.data_agent.Config import Config
from fastApi.data_agent.Database import Database
from fastApi.data_agent.Nl2SqlEngine import Nl2SqlEngine
from fastApi.data_agent.Nl2SqlPrompts import combined_prompt
from fastApi.orchestration.workflow import ProgressEvent
from sqlalchemy.exc import OperationalError


async def check_chart_name(ctx: Context):
    """Check if the chart name is exists."""
    template_name = await ctx.get("template_name")
    if template_name is None:
        return "Please select a chart template."
    return "Chart template selected."

async def check_connection(ctx: Context):
    """Check if the database connection is successful."""
    database = await ctx.get("database")
    try:
        with database.connect() as connection:
            connection.execute("SELECT 1")
        return True
    except OperationalError as e:
        return False


async def connect_to_db(ctx: Context) -> str:
    """Connect to the database and save the connection in the context."""
    config = Config("../../config.ini")
    ctx.write_event_to_stream(ProgressEvent(msg="connecting to the database..."))
    database = Database(config)
    await ctx.set("config", config)
    await ctx.set("database", database)
    return "Database connection established."


async def init_nl2sql_engine(ctx: Context) -> str:
    """Initializes the NL2SQL engine to let user convert natural language to SQL and select data from the database."""
    config = await ctx.get("config")
    database = await ctx.get("database")
    nl2sql_engine = Nl2SqlEngine(config, database)
    await ctx.set("nl2sql_engine", nl2sql_engine)
    return "NL2SQL engine initialized."


async def get_data_from_db(ctx: Context, user_query: str):
    """This function returns the data from the database based on the user query"""
    template_name = await ctx.get("template_name")
    query_message = create_query_message(user_query, template_name)
    nl2sql_engine = await ctx.get("nl2sql_engine")
    print("query_message",query_message)
    return nl2sql_engine.query(query_message)


def create_query_message(user_input: str, chart_name: str) -> str:
    return (
        f"User input: {user_input}\n"
        f"Chart example: {get_template_example_data_by_name(chart_name)}\n\n"
    )


def get_template_example_data_by_name(template_name: str):
    """this function returns the chart example by its name"""
    if template_name == "lineWithDataChart":
        return """
        "linewithDataChart": {
    "chart": {
      "height": 380,
      "type": "line",
      "zoom": {
        "enabled": false
      },
      "toolbar": {
        "show": false
      }
    },
    "colors": [
      "#556ee6",
      "#34c38f"
    ],
    "dataLabels": {
      "enabled": true
    },
    "stroke": {
      "width": [
        3,
        3
      ],
      "curve": "straight"
    },
    "series": [
      {
        "name": "High - 2018",
        "data": [
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
        "name": "Low - 2018",
        "data": [
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
    "title": {
      "text": "Average High & Low Temperature",
      "align": "left"
    },
    "grid": {
      "row": {
        "colors": [
          "transparent",
          "transparent"
        ],
        "opacity": 0.2
      },
      "borderColor": "#f1f1f1"
    },
    "markers": {
      "style": "inverted",
      "size": 6
    },
    "xaxis": {
      "categories": [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul"
      ],
      "title": {
        "text": "Month"
      }
    },
    "yaxis": {
      "title": {
        "text": "Temperature"
      },
      "min": 5,
      "max": 40
    },
    "legend": {
      "position": "top",
      "horizontalAlign": "right",
      "floating": true,
      "offsetY": -25,
      "offsetX": -5
    },
    "responsive": [
      {
        "breakpoint": 600,
        "options": {
          "chart": {
            "toolbar": {
              "show": false
            }
          },
          "legend": {
            "show": false
          }
        }
      }
    ]
  }
        """
    elif template_name == "basicColumChart":
        return """
        "basicColumChart": {
    "chart": {
      "height": 350,
      "type": "bar",
      "toolbar": {
        "show": false
      }
    },
    "plotOptions": {
      "bar": {
        "horizontal": false,
        "endingShape": "rounded",
        "columnWidth": "45%"
      }
    },
    "dataLabels": {
      "enabled": false
    },
    "stroke": {
      "show": true,
      "width": 2,
      "colors": [
        "transparent"
      ]
    },
    "colors": [
      "#34c38f",
      "#556ee6",
      "#f46a6a"
    ],
    "series": [
      {
        "name": "Net Profit",
        "data": [
          46,
          57,
          59,
          54,
          62,
          58,
          64,
          60,
          66
        ]
      },
      {
        "name": "Revenue",
        "data": [
          74,
          83,
          102,
          97,
          86,
          106,
          93,
          114,
          94
        ]
      },
      {
        "name": "Free Cash Flow",
        "data": [
          37,
          42,
          38,
          26,
          47,
          50,
          54,
          55,
          43
        ]
      }
    ],
    "xaxis": {
      "categories": [
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct"
      ]
    },
    "yaxis": {
      "title": {
        "text": "$ (thousands)"
      }
    },
    "fill": {
      "opacity": 1
    },
    "grid": {
      "borderColor": "#f1f1f1"
    },
    "tooltip": {
      "y": {
        "formatter": "(val) => '$ ' + val + ' thousands'"
      }
    }
  }
        """
    elif template_name == "dashedLineChart":
        return """
        "dashedLineChart": {
    "chart": {
      "height": 380,
      "type": "line",
      "zoom": {
        "enabled": false
      },
      "toolbar": {
        "show": false
      }
    },
    "colors": [
      "#556ee6",
      "#f46a6a",
      "#34c38f"
    ],
    "dataLabels": {
      "enabled": false
    },
    "stroke": {
      "width": [
        3,
        4,
        3
      ],
      "curve": "straight",
      "dashArray": [
        0,
        8,
        5
      ]
    },
    "series": [
      {
        "name": "Session Duration",
        "data": [
          45,
          52,
          38,
          24,
          33,
          26,
          21,
          20,
          6,
          8,
          15,
          10
        ]
      },
      {
        "name": "Page Views",
        "data": [
          36,
          42,
          60,
          42,
          13,
          18,
          29,
          37,
          36,
          51,
          32,
          35
        ]
      },
      {
        "name": "Total Visits",
        "data": [
          89,
          56,
          74,
          98,
          72,
          38,
          64,
          46,
          84,
          58,
          46,
          49
        ]
      }
    ],
    "title": {
      "text": "Page Statistics",
      "align": "left"
    },
    "markers": {
      "size": 0,
      "hover": {
        "sizeOffset": 6
      }
    },
    "xaxis": {
      "categories": [
        "01 Jan",
        "02 Jan",
        "03 Jan",
        "04 Jan",
        "05 Jan",
        "06 Jan",
        "07 Jan",
        "08 Jan",
        "09 Jan",
        "10 Jan",
        "11 Jan",
        "12 Jan"
      ]
    },
    "tooltip": {
      "y": [
        {
          "title": {
            "formatter": "(val) => val + ' (mins)'"
          }
        },
        {
          "title": {
            "formatter": "(val) => val + ' per session'"
          }
        },
        {
          "title": {
            "formatter": "(val) => val"
          }
        }
      ]
    },
    "grid": {
      "borderColor": "#f1f1f1"
    }
  }
        """
    elif template_name == "columnLabelChart":
        return """
        "columnlabelChart": {
    "chart": {
      "height": 350,
      "type": "bar",
      "toolbar": {
        "show": false
      }
    },
    "colors": [
      "#556ee6"
    ],
    "plotOptions": {
      "bar": {
        "dataLabels": {
          "position": "top"
        }
      }
    },
    "dataLabels": {
      "enabled": true,
      "formatter": "(val) => val + '%'",
      "offsetY": -20,
      "style": {
        "fontSize": "12px",
        "colors": [
          "#304758"
        ]
      }
    },
    "series": [
      {
        "name": "Inflation",
        "data": [
          2.5,
          3.2,
          5.0,
          10.1,
          4.2,
          3.8,
          3,
          2.4,
          4.0,
          1.2,
          3.5,
          0.8
        ]
      }
    ],
    "xaxis": {
      "categories": [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec"
      ],
      "position": "top",
      "labels": {
        "offsetY": -18
      },
      "axisBorder": {
        "show": false
      },
      "axisTicks": {
        "show": false
      },
      "crosshairs": {
        "fill": {
          "type": "gradient",
          "gradient": {
            "colorFrom": "#D8E3F0",
            "colorTo": "#BED1E6",
            "stops": [
              0,
              100
            ],
            "opacityFrom": 0.4,
            "opacityTo": 0.5
          }
        }
      },
      "tooltip": {
        "enabled": true,
        "offsetY": -35
      }
    },
    "fill": {
      "gradient": {
        "shade": "light",
        "type": "horizontal",
        "shadeIntensity": 0.25,
        "inverseColors": true,
        "opacityFrom": 1,
        "opacityTo": 1,
        "stops": [
          50,
          0,
          100,
          100
        ]
      }
    },
    "yaxis": {
      "axisBorder": {
        "show": false
      },
      "axisTicks": {
        "show": false
      },
      "labels": {
        "show": false,
        "formatter": "(val) => val + '%'"
      }
    },
    "title": {
      "text": "Monthly Inflation in Argentina, 2002",
      "floating": true,
      "offsetY": 320,
      "align": "center",
      "style": {
        "color": "#444"
      }
    }
  }
        """
    elif template_name == "barChart":
        return""""
        "barChart": {
    "chart": {
      "height": 350,
      "type": "bar",
      "toolbar": {
        "show": false
      }
    },
    "plotOptions": {
      "bar": {
        "horizontal": true
      }
    },
    "dataLabels": {
      "enabled": false
    },
    "series": [
      {
        "data": [
          380,
          430,
          450,
          475,
          550,
          584,
          780,
          1100,
          1220,
          1365
        ]
      }
    ],
    "colors": [
      "#34c38f"
    ],
    "xaxis": {
      "categories": [
        "South Korea",
        "Canada",
        "United Kingdom",
        "Netherlands",
        "Italy",
        "France",
        "Japan",
        "United States",
        "China",
        "Germany"
      ]
    },
    "grid": {
      "borderColor": "#f1f1f1"
    }
  }
        """
    elif template_name == "lineColumAreaChar":
        return """
        "lineColumAreaChart": {
    "chart": {
      "height": 350,
      "type": "line",
      "stacked": false,
      "toolbar": {
        "show": false
      }
    },
    "stroke": {
      "width": [
        0,
        2,
        4
      ],
      "curve": "smooth"
    },
    "plotOptions": {
      "bar": {
        "columnWidth": "50%"
      }
    },
    "colors": [
      "#f46a6a",
      "#556ee6",
      "#34c38f"
    ],
    "series": [
      {
        "name": "Team A",
        "type": "column",
        "data": [
          23,
          11,
          22,
          27,
          13,
          22,
          37,
          21,
          44,
          22,
          30
        ]
      },
      {
        "name": "Team B",
        "type": "area",
        "data": [
          44,
          55,
          41,
          67,
          22,
          43,
          21,
          41,
          56,
          27,
          43
        ]
      },
      {
        "name": "Team C",
        "type": "line",
        "data": [
          30,
          25,
          36,
          30,
          45,
          35,
          64,
          52,
          59,
          36,
          39
        ]
      }
    ],
    "fill": {
      "opacity": [
        0.85,
        0.25,
        1
      ],
      "gradient": {
        "inverseColors": false,
        "shade": "light",
        "type": "vertical",
        "opacityFrom": 0.85,
        "opacityTo": 0.55,
        "stops": [
          0,
          100,
          100,
          100
        ]
      }
    },
    "labels": [
      "01/01/2003",
      "02/01/2003",
      "03/01/2003",
      "04/01/2003",
      "05/01/2003",
      "06/01/2003",
      "07/01/2003",
      "08/01/2003",
      "09/01/2003",
      "10/01/2003",
      "11/01/2003"
    ],
    "markers": {
      "size": 0
    },
    "xaxis": {
      "type": "datetime"
    },
    "tooltip": {
      "shared": false,
      "intersect": true,
      "y": {
        "formatter": "(val) => val + ' points'"
      }
    }
  }
        """
    elif template_name == "simplePieChart":
        return """
          "simplePieChart": {
    "chart": {
      "height": 320,
      "type": "pie"
    },
    "series": [
      44,
      55,
      41,
      17,
      15
    ],
    "labels": [
      "Series 1",
      "Series 2",
      "Series 3",
      "Series 4",
      "Series 5"
    ],
    "colors": [
      "#34c38f",
      "#556ee6",
      "#f46a6a",
      "#50a5f1",
      "#f1b44c"
    ],
    "legend": {
      "show": true,
      "position": "bottom",
      "horizontalAlign": "center",
      "verticalAlign": "middle",
      "floating": false,
      "fontSize": "14px",
      "offsetX": 0,
      "offsetY": -10
    },
    "responsive": [
      {
        "breakpoint": 600,
        "options": {
          "chart": {
            "height": 240
          },
          "legend": {
            "show": false
          }
        }
      }
    ]
  }
        """
    elif template_name == "splineAreaChart":
        return """
        "splineAreaChart": {
    "chart": {
      "height": 350,
      "type": "area"
    },
    "dataLabels": {
      "enabled": false
    },
    "stroke": {
      "curve": "smooth",
      "width": 3
    },
    "series": [
      {
        "name": "series1",
        "data": [
          34,
          40,
          28,
          52,
          42,
          109,
          100
        ]
      },
      {
        "name": "series2",
        "data": [
          32,
          60,
          34,
          46,
          34,
          52,
          41
        ]
      }
    ],
    "colors": [
      "#556ee6",
      "#34c38f"
    ],
    "xaxis": {
      "type": "datetime",
      "categories": [
        "2018-09-19T00:00:00",
        "2018-09-19T01:30:00",
        "2018-09-19T02:30:00",
        "2018-09-19T03:30:00",
        "2018-09-19T04:30:00",
        "2018-09-19T05:30:00",
        "2018-09-19T06:30:00"
      ]
    },
    "grid": {
      "borderColor": "#f1f1f1"
    },
    "tooltip": {
      "x": {
        "format": "dd/MM/yy HH:mm"
      }
    }
  }
        """
    elif template_name == "donutChart":
        return """
         "donutChart": {
    "chart": {
      "height": 320,
      "type": "donut"
    },
    "series": [
      44,
      55,
      41,
      17,
      15
    ],
    "legend": {
      "show": true,
      "position": "bottom",
      "horizontalAlign": "center",
      "verticalAlign": "middle",
      "floating": false,
      "fontSize": "14px",
      "offsetX": 0,
      "offsetY": -10
    },
    "labels": [
      "Series 1",
      "Series 2",
      "Series 3",
      "Series 4",
      "Series 5"
    ],
    "colors": [
      "#34c38f",
      "#556ee6",
      "#f46a6a",
      "#50a5f1",
      "#f1b44c"
    ],
    "responsive": [
      {
        "breakpoint": 600,
        "options": {
          "chart": {
            "height": 240
          },
          "legend": {
            "show": false
          }
        }
      }
    ]
  }
        """
    elif template_name == "basicRadialBarChart":
        return """
        "basicRadialBarChart": {
    "chart": {
      "height": 380,
      "type": "radialBar"
    },
    "plotOptions": {
      "radialBar": {
        "dataLabels": {
          "name": {
            "fontSize": "22px"
          },
          "value": {
            "fontSize": "16px"
          },
          "total": {
            "show": true,
            "label": "Total",
            "formatter": "function(w) { return 249; }"
          }
        }
      }
    },
    "colors": [
      "#556ee6",
      "#34c38f",
      "#f46a6a",
      "#f1b44c"
    ],
    "series": [
      44,
      55,
      67,
      83
    ],
    "labels": [
      "Computer",
      "Tablet",
      "Laptop",
      "Mobile"
    ]
  }
        """
