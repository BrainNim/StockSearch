import React from 'react';
import { ThemeProvider } from 'styled-components';
import { NavigationContainer } from '@react-navigation/native';
import { createMaterialBottomTabNavigator } from '@react-navigation/material-bottom-tabs';
import Icon from 'react-native-vector-icons/dist/MaterialCommunityIcons';
import SearchScreen from './components/SearchScreen';
import EncyclopediaScreen from './pages/EncyclodiaScreen';
import NoticeScreen from './pages/NoticeScreen';
import theme from './theme/theme';

const Tab = createMaterialBottomTabNavigator();

function MyTabs() {
  return (
    <Tab.Navigator
      initialRouteName="종목검색"
      barStyle={{
        backgroundColor: '#FFFDFD',
        borderTopWidth: 1,
        borderColor: 'rgba(0, 0, 0, 0.26)',
      }}
      inactiveColor="rgba(0, 0, 0, 0.44)"
      activeColor="#703DE4">
      <Tab.Screen
        name="주식백과"
        style={{ marginBottom: 2 }}
        component={EncyclopediaScreen}
        options={{
          tabBarIcon: ({ color }) => (
            <Icon name="book-open-variant" color={color} size={24} />
          ),
        }}
      />
      <Tab.Screen
        name="종목검색"
        component={SearchScreen}
        options={{
          tabBarIcon: ({ color }) => (
            <Icon
              style={{ marginBottom: 2 }}
              name="magnify"
              color={color}
              size={24}
            />
          ),
        }}
      />
      <Tab.Screen
        name="게시판"
        component={NoticeScreen}
        options={{
          tabBarIcon: ({ color }) => (
            <Icon
              style={{ marginBottom: 2 }}
              name="clipboard-outline"
              color={color}
              size={24}
            />
          ),
        }}
      />
    </Tab.Navigator>
  );
}

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <NavigationContainer>
        <MyTabs />
      </NavigationContainer>
    </ThemeProvider>
  );
}
