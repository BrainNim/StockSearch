import React from 'react'
import { ThemeProvider } from 'styled-components'
import { NavigationContainer } from '@react-navigation/native'
import { createMaterialBottomTabNavigator } from '@react-navigation/material-bottom-tabs'
import Icon from 'react-native-vector-icons/dist/Ionicons'
import SearchScreen from './components/SearchScreen'
import EncyclopediaScreen from './pages/EncyclodiaScreen'
import NoticeScreen from './pages/NoticeScreen'
import theme from './theme/theme'



const Tab = createMaterialBottomTabNavigator()

function MyTabs () {
  return (
    <Tab.Navigator
      initialRouteName='종목검색'
      barStyle={{ backgroundColor: '#8FBBAF' }}
      inactiveColor='#6B7B8E'>
      <Tab.Screen
        name='주식백과'
        style={{ marginBottom: 2 }}
        component={EncyclopediaScreen}
        options={{
          tabBarIcon: ({ color }) => (
            <Icon name='newspaper-outline' color={color} size={24} />
          ),
        }}
      />
      <Tab.Screen
        name='종목검색'
        component={SearchScreen}
        options={{
          tabBarIcon: ({ color }) => (
            <Icon
              style={{ marginBottom: 2 }}
              name='search'
              color={color}
              size={24}
            />
          ),
        }}
      />
      <Tab.Screen
        name='게시판'
        component={NoticeScreen}
        options={{
          tabBarIcon: ({ color }) => (
            <Icon
              style={{ marginBottom: 2 }}
              name='ios-grid-sharp'
              color={color}
              size={24}
            />
          ),
        }}
      />
    </Tab.Navigator>
  )
}

export default function App () {
  return (
    <ThemeProvider theme={theme}>
    <NavigationContainer>
      <MyTabs />
    </NavigationContainer>
    </ThemeProvider>
  )
}
