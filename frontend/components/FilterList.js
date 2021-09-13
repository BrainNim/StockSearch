import React, { useState } from 'react';
import { Text, View, StyleSheet,Button } from 'react-native';
import Icon from 'react-native-vector-icons/dist/Ionicons';


export default function FilterList() {


  return (
    <View style={styles.view}>
      <RoundButton onPress={handlePress} text={<Icon name="add" size={42} />} />
      <Modal isVisible={isModalVisible}>
        <View style={{ flex: 1 }}>
        <Icon.Button title="close" onPress={handlePress}/>
            <View style={{ flex: 1 }}>
        </View>
         <View style={{ flex: 1 }}>
        </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  view: {
    display: 'flx',
    justifyContent: 'center',
    alignItems: 'center',
    flexD
  },
  add: {
    borderRadius: 40,
  },
});
