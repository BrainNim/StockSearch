import React, { useState } from 'react';
import { Text, View, StyleSheet,Button } from 'react-native';
import Icon from 'react-native-vector-icons/dist/Ionicons';
import RoundButton from './button/Button';
import Modal from 'react-native-modal';

export default function SearchScreen() {
  const [isModalVisible, setModalVisible] = useState(false);



  const handlePress = () => {
    setModalVisible(!isModalVisible);
  };
  return (
    <View style={styles.view}>
      <Text>종목검색!</Text>
      <RoundButton onPress={handlePress} text={<Icon name="add" size={42} />} />
      <Modal isVisible={isModalVisible} style={styles.modal}>
        <View style={styles.inner}>
        <Icon name="chevron-down-circle" size={30} onPress={handlePress} color="#8FBBAF"style={styles.close}/>
          <Text>조건 선택</Text>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  view: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  modal: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  inner : {
    backgroundColor:'white',
    width: '80%',
    height: '80%',
    borderRadius: 10,
    paddingVertical: 40,
    paddingHorizontal: 20,

  },
  close: { 
    position: 'absolute',
    right: 2,
    top: 4,
    width: 35,
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 1,
    paddingHorizontal: 1,
  },
});
