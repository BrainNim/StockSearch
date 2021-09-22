import React from 'react';
import { useState } from 'react';
import { Text, View, StyleSheet, Button } from 'react-native';
import Icon from 'react-native-vector-icons/dist/Ionicons';
import RoundButton from './button/Button';
import Modal from 'react-native-modal';
import FilterList from './FilterList';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HeaderTitle from './header/HeaderTitle';

function Main({ navigation }) {
  const [isModalVisible, setModalVisible] = useState(false);

  const handlePress = () => {
    navigation.navigate('Search');
  };
  return (
    <>
      <HeaderTitle icon="magnify" text="종목검색" />

      <View style={styles.view}>
        <View style={styles.addWrapper}>
          <RoundButton
            onPress={handlePress}
            text={<Icon name="add" size={42} />}
          />
          <Text style={styles.subtitle}>조건 추가하기</Text>
        </View>
        {/* <Modal isVisible={isModalVisible} style={styles.modal}> */}
        {/* <View style={styles.inner}>
          <Icon
            name='chevron-down-circle'
            size={30}
            onPress={handlePress}
            color='#8FBBAF'
            style={styles.close}
          />
          <Text>조건 선택</Text>
          <FilterList />
        </View> */}
        {/* </Modal> */}
      </View>
    </>
  );
}

const styles = StyleSheet.create({
  view: {
    paddingHorizontal: 20,
  },
  title: {
    fontSize: 25,
    fontWeight: '600',
  },
  subtitle: {
    fontSize: 25,
  },
  addWrapper: {
    alignItems: 'center',
    justifyContent: 'flex-start',
    flexDirection: 'row',
    textAlign: 'center',
    paddingVertical: 20,
  },
  modal: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  inner: {
    backgroundColor: 'white',
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

const Stack = createNativeStackNavigator();
export default function SearchScreen() {
  return (
    <Stack.Navigator
      screenOptions={{ presentation: 'modal' }}
      initialRouteName="main">
      <Stack.Screen
        name="main"
        options={{
          headerShown: false,
          title: `종목검색`,
          headerTitleStyle: {
            fontWeight: 'bold',
          },
        }}
        component={Main}
      />

      <Stack.Screen name="Search" component={FilterList} />
    </Stack.Navigator>
  );
}

//search screen 이 스택리턴
