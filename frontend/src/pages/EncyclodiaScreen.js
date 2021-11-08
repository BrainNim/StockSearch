import React from 'react';
import { View, Text } from 'react-native';
import HeaderTitle from '../components/header/HeaderTitle';

export default function EncyclopediaScreen() {
  return (
    <>
      <HeaderTitle icon="book-open-variant" text="주식백과" />
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <Text>주식 백과!</Text>
      </View>
    </>
  );
}
