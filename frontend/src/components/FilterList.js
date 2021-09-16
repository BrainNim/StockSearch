import React from 'react';
import { useState } from 'react';
import { Text, View, StyleSheet, FlatList } from 'react-native';
import { Button } from 'react-native-vector-icons/dist/Ionicons';


export default function FilterList() {
  const filter = [
    {
      name: 'MarketFilter',
      subfilter: [
        {
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
            type: 'day,inout',
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

  const [fidx, setIdx] = useState(0);
  const filterIdx = filter.map((v, idx) => ({ idx, name: v.name, setIdx , fidx}));
  return (
    <View style={styles.flexColum}>
      <View style={styles.view}>
        <FlatList data={filterIdx} renderItem={FilterMainItem} />
      </View>

      <View style={styles.view}>
        <FlatList data={filter[fidx].subfilter} renderItem={FilterItem} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  flexColum: {
    display: 'flex',
    flexDirection: 'row',
  },
  view: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    width: '50%',
    paddingVertical: 19,
  },
  main: {
    paddingVertical: 5,
    paddingHorizontal: 5,
  },
  sub: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    width: '50%',
    paddingVertical: 19,
    backgroundColor: '#FFE3DE'
  },
  button: {
    width: '100%',
    borderBottomRightRadius: 0,
    borderTopRightRadius: 0,
    backgroundColor: '#A3DDCB'
  },
  subbutton:{
    width: 140,
    backgroundColor: '#DBE6FD'
  },
  add: {
    borderRadius: 40,
  },
});

function FilterMainItem({ item }) {
  let style = styles.button
  if(item.idx === item.fidx){
    style = {...styles.button , backgroundColor: '#FFE3DE'}
  }
  const handlePress = () => {
    item.setIdx(item.idx);
  };

  return (
    <View style={styles.main}>
      <Button onPress={handlePress} style={style}>
        <Text>{item.name}</Text>
      </Button>
    </View>
  );
}


function FilterItem({ item }) {
  const handlePress = (itemName) => {
    console.log(itemName);
  };

  return (
    <View View style={styles.main}>
      <Button onPress={handlePress} style={styles.subbutton}>
      <Text  onPress={() => handlePress(item.name)}>{item.name}</Text>
      </Button>
    </View>
  );
}
