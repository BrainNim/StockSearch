import React from 'react';
import { useState } from 'react';
import { Text, View, StyleSheet, FlatList } from 'react-native';
import { Button } from 'react-native-vector-icons/dist/Ionicons';
import filter from '../mock';

export default function FilterList() {
  const [fidx, setIdx] = useState(0);
  const filterIdx = filter.map((v, idx) => ({
    idx,
    name: v.name,
    setIdx,
    fidx,
  }));
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
    backgroundColor: '#FFE3DE',
  },
  button: {
    width: '100%',
    borderBottomRightRadius: 0,
    borderTopRightRadius: 0,
    backgroundColor: '#A3DDCB',
  },
  subbutton: {
    width: 140,
    backgroundColor: '#DBE6FD',
  },
  add: {
    borderRadius: 40,
  },
});

function FilterMainItem({ item }) {
  let style = styles.button;
  if (item.idx === item.fidx) {
    style = { ...styles.button, backgroundColor: '#FFE3DE' };
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
  const handlePress = itemName => {
    console.log(itemName);
  };

  return (
    <View View style={styles.main}>
      <Button onPress={handlePress} style={styles.subbutton}>
        <Text onPress={() => handlePress(item.name)}>{item.name}</Text>
      </Button>
    </View>
  );
}
{
  /* <View style={styles.inner}>
<Icon
  name='chevron-down-circle'
  size={30}
  onPress={handlePress}
  color='#8FBBAF'
  style={styles.close}
/>
<Text>조건 선택</Text>
<FilterList />
</View> */
}
