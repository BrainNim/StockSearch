import React from 'react';
import { StyleSheet, TouchableOpacity, Text } from 'react-native';
import styled from 'styled-components/native';

export default function RoundButton({ text, onPress }) {
  return (
    <TouchableOpacity
      onPress={onPress}
      style={styles.button}
      activeOpacity={0.4}>
      <TextStyle>{text}</TextStyle>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: {
    backgroundColor: '#A590EF',
    alignItems: 'center',
    justifyContent: 'center',
    width: 46,
    height: 46,
    borderRadius: 35,

    ...Platform.select({
      ios: {
        shadowColor: 'rgba(0,0,0,0.2)',
        shadowOpacity: 1,
        shadowOffset: { height: 2, width: 2 },
        shadowRadius: 2,
      },

      android: {
        elevation: 0,
        marginHorizontal: 30,
      },
    }),
  },
});

const TextStyle = styled.Text`
  font-size: 18px;
  text-align: center;
  color: #ffffff;
`;
