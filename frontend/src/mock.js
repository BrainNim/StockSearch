const filter = [
  {
    name: 'MarketFilter',
    subfilter: [
      {
        //복수선택가능
        //컴마로해서
        name: 'market',
        input: {
          type: 'market',
          data_format: 'KOSPI,KOSDAQ',
        },
      },
      {
        name: 'category',
        input: {
          type: 'category',
          data_format: '식품,car,화학',
        },
      },
    ],
  },
  {
    name: 'PriceFilter',
    subfilter: [
      {
        name: 'updown',
        input: {
          type: 'min,max',
          data_format: 'int,int',
        },
      },
      {
        name: 'compare_mean',
        input: {
          type: 'day,times,updown',
          data_format: 'int,flt,str',
        },
      },
      {
        name: 'compare_max',
        input: {
          type: 'times',
          data_format: 'flt',
        },
      },
      {
        name: 'dist_max',
        input: {
          type: 'day,input',
          data_format: 'int,str',
        },
      },
    ],
  },
  {
    name: 'VolumeFilter',
    subfilter: [
      {
        name: 'updown',
        input: {
          type: 'min,max',
          data_format: 'int,int',
        },
      },
      {
        name: 'compare_mean',
        input: {
          type: 'day,times,updown',
          data_format: 'int,flt,str',
        },
      },
    ],
  },
  {
    name: 'PBRFilter',
    subfilter: [
      {
        name: 'updown',
        input: {
          type: 'min,max',
          data_format: 'flt,flt',
        },
      },
      {
        name: 'top',
        input: {
          type: 'topdown,N',
          data_format: 'str,int',
        },
      },
    ],
  },
  {
    name: 'PERFilter',
    subfilter: [
      {
        name: 'updown',
        input: {
          type: 'min,max',
          data_format: 'flt,flt',
        },
      },
      {
        name: 'top',
        input: {
          type: 'topdown,N',
          data_format: 'str,int',
        },
      },
    ],
  },
  {
    name: 'ROAFilter',
    subfilter: [
      {
        name: 'updown',
        input: {
          type: 'min,max',
          data_format: 'flt,flt',
        },
      },
      {
        name: 'top',
        input: {
          type: 'topdown,N',
          data_format: 'str,int',
        },
      },
    ],
  },
  {
    name: 'ROEFilter',
    subfilter: [
      {
        name: 'updown',
        input: {
          type: 'min,max',
          data_format: 'flt,flt',
        },
      },
      {
        name: 'top',
        input: {
          type: 'topdown,N',
          data_format: 'str,int',
        },
      },
    ],
  },
  {
    name: 'CrossFilter',
    subfilter: [
      {
        name: 'goldencross',
        input: {
          type: 'short,long',
          data_format: 'int,int',
        },
      },
      {
        name: 'deadcross',
        input: {
          type: 'short,long',
          data_format: 'int,int',
        },
      },
    ],
  },
];

export default filter;
