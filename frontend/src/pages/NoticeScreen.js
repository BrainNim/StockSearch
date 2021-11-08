import React from 'react';
import { View, Text } from 'react-native';
import HeaderTitle from '../components/header/HeaderTitle';

export default function NoticeScreen() {
  return (
    <>
      <HeaderTitle icon="clipboard-outline" text="게시판" />
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <Text>notice board!</Text>
      </View>
    </>
  );
}
