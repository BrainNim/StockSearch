import React from 'react';
import { useState } from 'react';
import { Text, View, StyleSheet } from 'react-native';
import Icon from 'react-native-vector-icons/dist/Ionicons';
import RoundButton from './button/Button';
import Modal from 'react-native-modal';
import FilterList from './FilterList';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HeaderTitle from './header/HeaderTitle';
import styled from 'styled-components/native';

function Main({ navigation }) {
  const [isModalVisible, setModalVisible] = useState(true);

  const handlePress = () => {
    setModalVisible(!isModalVisible);
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
        <StyleModal
          isVisible={isModalVisible}
          customBackdrop={
            <Backdrop onPress={() => setModalVisible(!isModalVisible)} />
          }>
          <View style={styles.inner}>
            <Icon
              name="chevron-down-circle"
              size={30}
              onPress={handlePress}
              color="#8FBBAF"
              style={styles.close}
            />
            <Text>조건 선택</Text>
            <FilterList />
          </View>
        </StyleModal>
      </View>
    </>
  );
}
const Backdrop = styled.TouchableOpacity`
  width: 100%;
  height: 80%;
  background-color: black;
  opacity: 0.7;
`;

const StyleModal = styled(Modal)`
  position: absolute;
  bottom: 0;
  margin: 0;
`;

const styles = StyleSheet.create({
  view: {
    paddingHorizontal: 20,
  },
  title: {
    fontSize: 25,
    fontWeight: '600',
  },
  subtitle: {
    fontSize: 17,
    fontWeight: 'bold',
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
    width: '100%',
    height: '80%',
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
