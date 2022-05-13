$(function() {
  /* ChartJS
   * -------
   * Data and config for chartjs
   */
  'use strict';
  var data = {
    labels: ["Online", "Food", "Home", "Recharge", "Health", "Festival", "Others"],
    datasets: [{
      label: 'Cash Amount',
      data: [2000, 5000, 3000, 9000, 2000, 3000, 4000],
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(100, 159, 64, 0.2)'
      ],
      borderColor: [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)',
        'rgba(100, 159, 64, 1)'
      ],
      borderWidth: 1,
      fill: false
    }]
  };

  var data1 = {
    labels: ["Online", "Food", "Home", "Recharge", "Health", "Festival", "Others"],
    datasets: [{
      label: 'Credit Card Amount',
      data: [2000, 10000, 3000, 3500, 2000, 3000, 4000],
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(100, 159, 64, 0.2)'
      ],
      borderColor: [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)',
        'rgba(100, 159, 64, 1)'
      ],
      borderWidth: 1,
      fill: false
    }]
  };

  var data2 = {
    labels: ["Online", "Food", "Home", "Recharge", "Health", "Festival", "Others"],
    datasets: [{
      label: 'Debit Card Amount',
      data: [2000, 5000, 3000, 2000, 2000, 11000, 4000],
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(100, 159, 64, 0.2)'
      ],
      borderColor: [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)',
        'rgba(100, 159, 64, 1)'
      ],
      borderWidth: 1,
      fill: false
    }]
  };

  var data3 = {
    labels: ["Online", "Food", "Home", "Recharge", "Health", "Festival", "Others"],
    datasets: [{
      label: 'UPI Amount',
      data: [11000, 4000, 3000, 4000, 2000, 3000, 4000],
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(100, 159, 64, 0.2)'
      ],
      borderColor: [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)',
        'rgba(100, 159, 64, 1)'
      ],
      borderWidth: 1,
      fill: false
    }]
  };

  var multiLineData = {
    labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
    datasets: [{
        label: 'Dataset 1',
        data: [12, 19, 3, 5, 2, 3],
        borderColor: [
          '#587ce4'
        ],
        borderWidth: 2,
        fill: false
      },
      {
        label: 'Dataset 2',
        data: [5, 23, 7, 12, 42, 23],
        borderColor: [
          '#ede190'
        ],
        borderWidth: 2,
        fill: false
      },
      {
        label: 'Dataset 3',
        data: [15, 10, 21, 32, 12, 33],
        borderColor: [
          '#f44252'
        ],
        borderWidth: 2,
        fill: false
      }
    ]
  };
  var options = {
    scales: {
      yAxes: [{
        ticks: {
          beginAtZero: true
        }
      }]
    },
    legend: {
      display: false
    },
    elements: {
      point: {
        radius: 0
      }
    }

  };
  var doughnutPieData = {
    datasets: [{
      data: [40, 30, 15, 10, 5],
      backgroundColor: [
        'rgba(255, 99, 132, 0.5)',
        'rgba(54, 162, 235, 0.5)',
        'rgba(255, 206, 86, 0.5)',
        'rgba(75, 192, 192, 0.5)',
        'rgba(153, 102, 255, 0.5)',
        'rgba(255, 159, 64, 0.5)'
      ],
      borderColor: [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
      ],
    }],

    // These labels appear in the legend and in the tooltips when hovering different arcs
    labels: [
      'Cash',
      'Credit',
      'Debit',
      'Phonepe',
      'GPay',
    ]
  };
  var doughnutPieOptions = {
    responsive: true,
    animation: {
      animateScale: true,
      animateRotate: true
    }
  };


// Area Charts Start
  
  var areaData = {
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    datasets: [{
      label: 'Amount Spend',
      data: [12, 13, 11, 10, 12, 13, 11, 10, 12, 13, 11, 10, 12, 13, 11, 10],
      backgroundColor: [
        'rgba(54, 162, 235, 0.2)',
      ],
      borderColor: [
        'rgba(54, 162, 235, 1)',
      ],
      borderWidth: 2,
      fill: true, // 3: no fill
    }]
  };

  var areaOptions = {
    plugins: {
      filler: {
        propagate: true
      }
    },
    scales: {
      
      xAxes: [{
        gridLines: {
          display: false
        },
        scaleLabel: {
          display: true,
          labelString: 'Months'
        },
        ticks:{
          maxTicksLimit: 6
        }
      }],
      yAxes: [{
        ticks: {
          maxTicksLimit: 5
        },
        scaleLabel: {
          display: true,
          labelString: 'Amount'
        }
      }]     
    }
  }

  var areaDatacrypto = {
    labels: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    datasets: [{
      label: 'Crypto Transactions',
      data: [12, 17, 11, 15, 12, 13, 12, 17, 15, 17,12, 17, 11, 15, 12, 13, 12, 17, 15, 17,12, 17, 11, 15, 12, 13, 12, 17, 15, 17,12],
      backgroundColor: [
        'rgba(54, 162, 235, 0.2)',
      ],
      borderColor: [
        'rgba(54, 162, 235, 1)',
      ],
      borderWidth: 1,
      fill: true, // 3: no fill
    }]
  };

  var areaOptionscrypto = {
    plugins: {
      filler: {
        propagate: true
      }
    },
    elements: {
      point: {
        radius: 2
      }
    },
    scales: {
      
      xAxes: [{
        gridLines: {
          display: false
        },
        scaleLabel: {
          display: true,
          labelString: 'Days'
        },
        ticks:{
          maxTicksLimit: 10
        }
      }],
      yAxes: [{
        ticks: {
          maxTicksLimit: 4
        },
        scaleLabel: {
          display: true,
          labelString: 'Amount'
        }
      }]     
    }
  }

  var areaDataonline = {
    labels: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    datasets: [{
      label: 'Online Shopping Transactions',
      data: [12, 17, 11, 15, 12, 13, 12, 17, 15, 17,12, 17, 11, 15, 12, 13, 12, 17, 15, 17,12, 17, 11, 15, 12, 13, 12, 17, 15, 17,12],
      backgroundColor: [
        'rgba(158, 87, 214, 0.2)',
      ],
      borderColor: [
        'rgba(158, 87, 214, 1)',
      ],
      borderWidth: 1,
      fill: true, // 3: no fill
    }]
  };

  var areaOptionsonline = {
    plugins: {
      filler: {
        propagate: true
      }
    },
    elements: {
      point: {
        radius: 2
      }
    },
    scales: {
      
      xAxes: [{
        gridLines: {
          display: false
        },
        scaleLabel: {
          display: true,
          labelString: 'Days'
        },
        ticks:{
          maxTicksLimit: 10
        }
      }],
      yAxes: [{
        ticks: {
          maxTicksLimit: 4
        },
        scaleLabel: {
          display: true,
          labelString: 'Amount'
        }
      }] 
    }

  }

  var areaDatafood = {
    labels: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    datasets: [{
      label: 'Food Transactions',
      data: [12, 17, 11, 15, 12, 13, 12, 17, 15, 17,12, 17, 11, 15, 12, 13, 12, 17, 15, 17,12, 17, 11, 15, 12, 13, 12, 17, 15, 17,12],
      backgroundColor: [
        'rgba(93, 194, 71, 0.2)',
      ],
      borderColor: [
        'rgba(93, 194, 71, 1)',
      ],
      borderWidth: 1,
      fill: true, // 3: no fill
    }]
  };

  var areaOptionsfood = {
    plugins: {
      filler: {
        propagate: true
      }
    },
    elements: {
      point: {
        radius: 2
      }
    },
    scales: {
      
      xAxes: [{
        gridLines: {
          display: false
        },
        scaleLabel: {
          display: true,
          labelString: 'Days'
        },
        ticks:{
          maxTicksLimit: 10
        }
      }],
      yAxes: [{
        ticks: {
          maxTicksLimit: 4
        },
        scaleLabel: {
          display: true,
          labelString: 'Amount'
        }
      }] 
    }

  }

  var areaDatahome = {
    labels: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    datasets: [{
      label: 'Home Transactions',
      data: [12, 17, 11, 15, 12, 13, 12, 17, 15, 17,12, 17, 11, 15, 12, 13, 12, 17, 15, 17,12, 17, 11, 15, 12, 13, 12, 17, 15, 17,12],
      backgroundColor: [
        'rgba(75, 73, 166, 0.2)',
      ],
      borderColor: [
        'rgba(75, 73, 166, 1)',
      ],
      borderWidth: 1,
      fill: true, // 3: no fill
    }]
  };

  var areaOptionshome = {
    plugins: {
      filler: {
        propagate: true
      }
    },
    elements: {
      point: {
        radius: 2
      }
    },
    scales: {
      
      xAxes: [{
        gridLines: {
          display: false
        },
        scaleLabel: {
          display: true,
          labelString: 'Days'
        },
        ticks:{
          maxTicksLimit: 10
        }
      }],
      yAxes: [{
        ticks: {
          maxTicksLimit: 4
        },
        scaleLabel: {
          display: true,
          labelString: 'Amount'
        }
      }] 
    }

  }

  var areaDatarecharge = {
    labels: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    datasets: [{
      label: 'Recharge Transactions',
      data: [12, 17, 11, 15, 12, 13, 12, 17, 15, 17,12, 17, 11, 15, 12, 13, 12, 17, 15, 17,12, 17, 11, 15, 12, 13, 12, 17, 15, 17,12],
      backgroundColor: [
        'rgba(70, 157, 179, 0.2)',
      ],
      borderColor: [
        'rgba(70, 157, 179, 1)',
      ],
      borderWidth: 1,
      fill: true, // 3: no fill
    }]
  };

  var areaOptionsrecharge = {
    plugins: {
      filler: {
        propagate: true
      }
    },
    elements: {
      point: {
        radius: 2
      }
    },
    scales: {
      
      xAxes: [{
        gridLines: {
          display: false
        },
        scaleLabel: {
          display: true,
          labelString: 'Days'
        },
        ticks:{
          maxTicksLimit: 10
        }
      }],
      yAxes: [{
        ticks: {
          maxTicksLimit: 4
        },
        scaleLabel: {
          display: true,
          labelString: 'Amount'
        }
      }] 
    }

  }

  var areaDatahealth = {
    labels: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    datasets: [{
      label: 'Health Transactions',
      data: [12, 17, 11, 15, 12, 13, 12, 17, 15, 17,12, 17, 11, 15, 12, 13, 12, 17, 15, 17,12, 17, 11, 15, 12, 13, 12, 17, 15, 17,12],
      backgroundColor: [
        'rgba(241, 168, 70, 0.2)',
      ],
      borderColor: [
        'rgba(241, 168, 70, 1)',
      ],
      borderWidth: 1,
      fill: true, // 3: no fill
    }]
  };

  var areaOptionshealth = {
    plugins: {
      filler: {
        propagate: true
      }
    },
    elements: {
      point: {
        radius: 2
      }
    },
    scales: {
      
      xAxes: [{
        gridLines: {
          display: false
        },
        scaleLabel: {
          display: true,
          labelString: 'Days'
        },
        ticks:{
          maxTicksLimit: 10
        }
      }],
      yAxes: [{
        ticks: {
          maxTicksLimit: 4
        },
        scaleLabel: {
          display: true,
          labelString: 'Amount'
        }
      }] 
    }

  }

  var areaDatafestival = {
    labels: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    datasets: [{
      label: 'Festival Transactions',
      data: [12, 17, 11, 15, 12, 13, 12, 17, 15, 17,12, 17, 11, 15, 12, 13, 12, 17, 15, 17,12, 17, 11, 15, 12, 13, 12, 17, 15, 17,12],
      backgroundColor: [
        'rgba(193, 42, 101, 0.2)',
      ],
      borderColor: [
        'rgba(193, 42, 101, 1)',
      ],
      borderWidth: 1,
      fill: true, // 3: no fill
    }]
  };

  var areaOptionsfestival = {
    plugins: {
      filler: {
        propagate: true
      }
    },
    elements: {
      point: {
        radius: 2
      }
    },
    scales: {
      
      xAxes: [{
        gridLines: {
          display: false
        },
        scaleLabel: {
          display: true,
          labelString: 'Days'
        },
        ticks:{
          maxTicksLimit: 10
        }
      }],
      yAxes: [{
        ticks: {
          maxTicksLimit: 4
        },
        scaleLabel: {
          display: true,
          labelString: 'Amount'
        }
      }] 
    }

  }

  var areaDataother = {
    labels: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    datasets: [{
      label: 'Other Transactions',
      data: [12, 17, 11, 15, 12, 13, 12, 17, 15, 17,12, 17, 11, 15, 12, 13, 12, 17, 15, 17,12, 17, 11, 15, 12, 13, 12, 17, 15, 17,12],
      backgroundColor: [
        'rgba(100, 54, 23, 0.2)',
      ],
      borderColor: [
        'rgba(100, 54, 23, 1)',
      ],
      borderWidth: 1,
      fill: true, // 3: no fill
    }]
  };

  var areaOptionsother = {
    plugins: {
      filler: {
        propagate: true
      }
    },
    elements: {
      point: {
        radius: 2
      }
    },
    scales: {
      
      xAxes: [{
        gridLines: {
          display: false
        },
        scaleLabel: {
          display: true,
          labelString: 'Days'
        },
        ticks:{
          maxTicksLimit: 10
        }
      }],
      yAxes: [{
        ticks: {
          maxTicksLimit: 4
        },
        scaleLabel: {
          display: true,
          labelString: 'Amount'
        }
      }] 
    }

  }

// Area Charts for all pages done

  var multiAreaData = {
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    datasets: [{
        label: 'Facebook',
        data: [8, 11, 13, 15, 12, 13, 16, 15, 13, 19, 11, 14],
        borderColor: ['rgba(255, 99, 132, 0.5)'],
        backgroundColor: ['rgba(255, 99, 132, 0.5)'],
        borderWidth: 1,
        fill: true
      },
      {
        label: 'Twitter',
        data: [7, 17, 12, 16, 14, 18, 16, 12, 15, 11, 13, 9],
        borderColor: ['rgba(54, 162, 235, 0.5)'],
        backgroundColor: ['rgba(54, 162, 235, 0.5)'],
        borderWidth: 1,
        fill: true
      },
      {
        label: 'Linkedin',
        data: [6, 14, 16, 20, 12, 18, 15, 12, 17, 19, 15, 11],
        borderColor: ['rgba(255, 206, 86, 0.5)'],
        backgroundColor: ['rgba(255, 206, 86, 0.5)'],
        borderWidth: 1,
        fill: true
      }
    ]
  };

  var multiAreaOptions = {
    plugins: {
      filler: {
        propagate: true
      }
    },
    elements: {
      point: {
        radius: 0
      }
    },
    scales: {
      xAxes: [{
        gridLines: {
          display: false
        }
      }],
      yAxes: [{
        gridLines: {
          display: false
        }
      }]
    }
  }

  var scatterChartData = {
    datasets: [{
        label: 'First Dataset',
        data: [{
            x: -10,
            y: 0
          },
          {
            x: 0,
            y: 3
          },
          {
            x: -25,
            y: 5
          },
          {
            x: 40,
            y: 5
          }
        ],
        backgroundColor: [
          'rgba(255, 99, 132, 0.2)'
        ],
        borderColor: [
          'rgba(255,99,132,1)'
        ],
        borderWidth: 1
      },
      {
        label: 'Second Dataset',
        data: [{
            x: 10,
            y: 5
          },
          {
            x: 20,
            y: -30
          },
          {
            x: -25,
            y: 15
          },
          {
            x: -10,
            y: 5
          }
        ],
        backgroundColor: [
          'rgba(54, 162, 235, 0.2)',
        ],
        borderColor: [
          'rgba(54, 162, 235, 1)',
        ],
        borderWidth: 1
      }
    ]
  }

  var scatterChartOptions = {
    scales: {
      xAxes: [{
        type: 'linear',
        position: 'bottom'
      }]
    }
  }
  // Get context with jQuery - using jQuery's .get() method.
  if ($("#barChart").length) {
    var barChartCanvas = $("#barChart").get(0).getContext("2d");
    // This will get the first returned node in the jQuery collection.
    var barChart = new Chart(barChartCanvas, {
      type: 'bar',
      data: data,
      options: options
    });
  }

  if ($("#barChartcredit").length) {
    var barChartCanvascredit = $("#barChartcredit").get(0).getContext("2d");
    // This will get the first returned node in the jQuery collection.
    var barChartcredit = new Chart(barChartCanvascredit, {
      type: 'bar',
      data: data1,
      options: options
    });
  }

  if ($("#barChartdebit").length) {
    var barChartCanvasdebit = $("#barChartdebit").get(0).getContext("2d");
    // This will get the first returned node in the jQuery collection.
    var barChartdebit = new Chart(barChartCanvasdebit, {
      type: 'bar',
      data: data2,
      options: options
    });
  }

  if ($("#barChartUPI").length) {
    var barChartCanvasUPI = $("#barChartUPI").get(0).getContext("2d");
    // This will get the first returned node in the jQuery collection.
    var barChartUPI = new Chart(barChartCanvasUPI, {
      type: 'bar',
      data: data3,
      options: options
    });
  }

  if ($("#lineChart").length) {
    var lineChartCanvas = $("#lineChart").get(0).getContext("2d");
    var lineChart = new Chart(lineChartCanvas, {
      type: 'line',
      data: data,
      options: options
    });
  }

  if ($("#linechart-multi").length) {
    var multiLineCanvas = $("#linechart-multi").get(0).getContext("2d");
    var lineChart = new Chart(multiLineCanvas, {
      type: 'line',
      data: multiLineData,
      options: options
    });
  }

  if ($("#areachart-multi").length) {
    var multiAreaCanvas = $("#areachart-multi").get(0).getContext("2d");
    var multiAreaChart = new Chart(multiAreaCanvas, {
      type: 'line',
      data: multiAreaData,
      options: multiAreaOptions
    });
  }

  if ($("#doughnutChart").length) {
    var doughnutChartCanvas = $("#doughnutChart").get(0).getContext("2d");
    var doughnutChart = new Chart(doughnutChartCanvas, {
      type: 'doughnut',
      data: doughnutPieData,
      options: doughnutPieOptions
    });
  }

  if ($("#pieChart").length) {
    var pieChartCanvas = $("#pieChart").get(0).getContext("2d");
    var pieChart = new Chart(pieChartCanvas, {
      type: 'pie',
      data: doughnutPieData,
      options: doughnutPieOptions
    });
  }

  // Area Chart Starts

  if ($("#areaChart").length) {
    var areaChartCanvas = $("#areaChart").get(0).getContext("2d");
    var areaChart = new Chart(areaChartCanvas, {
      type: 'line',
      data: areaData,
      options: areaOptions
    });
  }

  if ($("#areaChartcrypto").length) {
    var areaChartCanvascrypto = $("#areaChartcrypto").get(0).getContext("2d");
    var areaChartcrypto = new Chart(areaChartCanvascrypto, {
      type: 'line',
      data: areaDatacrypto,
      options: areaOptionscrypto
    });
  }

  if ($("#areaChartonline").length) {
    var areaChartCanvasonline = $("#areaChartonline").get(0).getContext("2d");
    var areaChartonline = new Chart(areaChartCanvasonline, {
      type: 'line',
      data: areaDataonline,
      options: areaOptionsonline
    });
  }

  if ($("#areaChartfood").length) {
    var areaChartCanvasfood = $("#areaChartfood").get(0).getContext("2d");
    var areaChartfood = new Chart(areaChartCanvasfood, {
      type: 'line',
      data: areaDatafood,
      options: areaOptionsfood
    });
  }

  if ($("#areaCharthome").length) {
    var areaChartCanvashome = $("#areaCharthome").get(0).getContext("2d");
    var areaCharthome = new Chart(areaChartCanvashome, {
      type: 'line',
      data: areaDatahome,
      options: areaOptionshome
    });
  }

  if ($("#areaChartrecharge").length) {
    var areaChartCanvasrecharge = $("#areaChartrecharge").get(0).getContext("2d");
    var areaChartrecharge = new Chart(areaChartCanvasrecharge, {
      type: 'line',
      data: areaDatarecharge,
      options: areaOptionsrecharge
    });
  }

  if ($("#areaCharthealth").length) {
    var areaChartCanvashealth = $("#areaCharthealth").get(0).getContext("2d");
    var areaCharthealth = new Chart(areaChartCanvashealth, {
      type: 'line',
      data: areaDatahealth,
      options: areaOptionshealth
    });
  }

  if ($("#areaChartfestival").length) {
    var areaChartCanvasfestival = $("#areaChartfestival").get(0).getContext("2d");
    var areaChartfestival = new Chart(areaChartCanvasfestival, {
      type: 'line',
      data: areaDatafestival,
      options: areaOptionsfestival
    });
  }

  if ($("#areaChartother").length) {
    var areaChartCanvasother = $("#areaChartother").get(0).getContext("2d");
    var areaChartother = new Chart(areaChartCanvasother, {
      type: 'line',
      data: areaDataother,
      options: areaOptionsother
    });
  }

  // Area Chart Ends

  if ($("#scatterChart").length) {
    var scatterChartCanvas = $("#scatterChart").get(0).getContext("2d");
    var scatterChart = new Chart(scatterChartCanvas, {
      type: 'scatter',
      data: scatterChartData,
      options: scatterChartOptions
    });
  }

  if ($("#browserTrafficChart").length) {
    var doughnutChartCanvas = $("#browserTrafficChart").get(0).getContext("2d");
    var doughnutChart = new Chart(doughnutChartCanvas, {
      type: 'doughnut',
      data: browserTrafficData,
      options: doughnutPieOptions
    });
  }
});