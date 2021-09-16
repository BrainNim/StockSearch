import React from 'react';
import { View, Text, Button } from 'react-native';

export default function FilterItem({ item }) {
  const handlePress = (itemName) => {
    console.log(itemName);
  };

  return (
    <View>
      <Text  onPress={() => handlePress(item.name)}>{item.name}</Text>
    </View>
  );
}
