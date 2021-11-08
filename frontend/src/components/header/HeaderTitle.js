import React from 'react';
import { Header } from 'react-native-elements/dist/header/Header';
import Icon from 'react-native-vector-icons/dist/MaterialCommunityIcons';

export default function HeaderTitle({ text, icon }) {
  return (
    <Header
      placement="left"
      leftComponent={<Icon name={icon} size={22} />}
      centerComponent={{
        text,
        style: { fontSize: 18, fontWeight: 'bold' },
      }}
      containerStyle={{
        paddingVertical: 30,
        paddingHorizontal: 23,
      }}
    />
  );
}
